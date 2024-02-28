#!/usr/bin/env python3

"""Structure Model Module"""

import sys
import zlib
import json
from typing import Any, Callable, Generator

from palworld_save_tools.gvas import GvasFile
from palworld_save_tools.palsav import decompress_sav_to_gvas
from palworld_save_tools.paltypes import PALWORLD_TYPE_HINTS
from palworld_save_tools.archive import FArchiveReader, FArchiveWriter
from palworld_save_tools.rawdata import character, group

from .world_types import Player, Pal, Guild
from .logger import log

PALWORLD_CUSTOM_PROPERTIES: dict[
    str,
    tuple[
        Callable[[FArchiveReader, str, int, str], dict[str, Any]],
        Callable[[FArchiveWriter, str, dict[str, Any]], int],
    ],
] = {
    ".worldSaveData.GroupSaveDataMap": (group.decode, group.encode),
    ".worldSaveData.CharacterSaveParameterMap.Value.RawData": (
        character.decode,
        character.encode,
    ),
}

GuildGeneratorType = Generator[dict[str, str], Any, None]


def skip_decode(
    reader: FArchiveReader, type_name: str, size: int, path: str
) -> dict[str, Any]:
    """NOTE: Requires documentation from the original owner."""
    if type_name == "ArrayProperty":
        array_type = reader.fstring()
        value = {
            "skip_type": type_name,
            "array_type": array_type,
            "id": reader.optional_guid(),
            "value": reader.read(size),
        }
    elif type_name == "MapProperty":
        key_type = reader.fstring()
        value_type = reader.fstring()
        _id = reader.optional_guid()
        value = {
            "skip_type": type_name,
            "key_type": key_type,
            "value_type": value_type,
            "id": _id,
            "value": reader.read(size),
        }
    elif type_name == "StructProperty":
        value = {
            "skip_type": type_name,
            "struct_type": reader.fstring(),
            "struct_id": reader.guid(),
            "id": reader.optional_guid(),
            "value": reader.read(size),
        }
    else:
        raise TypeError(
            f"Expected ArrayProperty or MapProperty or StructProperty, got {type_name} in {path}"
        )
    return value


def skip_encode(
    writer: FArchiveWriter, property_type: str, properties: dict[str, Any]
) -> int:
    """NOTE: Requires documentation from the original owner."""
    if property_type == "ArrayProperty":
        del properties["custom_type"]
        del properties["skip_type"]
        writer.fstring(properties["array_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    elif property_type == "MapProperty":
        del properties["custom_type"]
        del properties["skip_type"]
        writer.fstring(properties["key_type"])
        writer.fstring(properties["value_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    elif property_type == "StructProperty":
        del properties["custom_type"]
        del properties["skip_type"]
        writer.fstring(properties["struct_type"])
        writer.guid(properties["struct_id"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    else:
        raise TypeError(
            f"Expected ArrayProperty or MapProperty or StructProperty, got {property_type}"
        )


PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSaveData"] = (
    skip_decode,
    skip_encode,
)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.FoliageGridSaveDataMap"] = (
    skip_decode,
    skip_encode,
)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.MapObjectSpawnerInStageSaveData"] = (
    skip_decode,
    skip_encode,
)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData"] = (
    skip_decode,
    skip_encode,
)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.DynamicItemSaveData"] = (
    skip_decode,
    skip_encode,
)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterContainerSaveData"] = (
    skip_decode,
    skip_encode,
)


def convert_sav(file: str) -> str | dict[str, Any]:
    """NOTE: Requires documentation from the original owner."""
    if file.endswith(".sav.json"):
        log("Loading...")
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    log("Converting...")
    try:
        with open(file, "rb") as f:
            data: bytes = f.read()
            raw_gvas, _ = decompress_sav_to_gvas(data)
        gvas_file: GvasFile = GvasFile.read(
            raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES
        )
    except zlib.error:
        log("This .sav file is corrupted. :(", "ERROR")
        sys.exit(1)
    # return json.dumps(gvas_file.dump(), cls=CustomEncoder)
    return gvas_file.properties


def structure_player(converted: dict[str, Any]) -> list[dict[str, Any]]:
    """NOTE: Requires documentation from the original owner."""
    log("Structuring players...")
    if not converted["worldSaveData"]["value"].get("CharacterSaveParameterMap"):
        return []
    uid_character: Generator[Any, Any, Any] = (
        (
            c["key"]["PlayerUId"]["value"],
            c["value"]["RawData"]["value"]["object"]["SaveParameter"]["value"],
        )
        for c in converted["worldSaveData"]["value"]["CharacterSaveParameterMap"][
            "value"
        ]
    )
    players: list[dict[str, Any]] = []
    pals: list[dict[str, Any]] = []
    for uid, c in uid_character:
        if c.get("IsPlayer") and c["IsPlayer"]["value"]:
            players.append(Player(uid, c).to_dict())
        else:
            if not c.get("OwnerPlayerUId"):
                continue
            pals.append(Pal(c).to_dict())
    for pal in pals:
        for player in players:
            if player["player_uid"] == pal["owner"]:
                pal.pop("owner")
                player["pals"].append(pal)
                break
    sorted_players: list[dict[str, Any]] = sorted(players, key=lambda p: p["level"], reverse=True)
    return list(sorted_players)


def structure_guild(converted: dict[str, Any], filetime: int = -1) -> list[dict[str, Any]]:
    """NOTE: Requires documentation from the original owner."""
    log("Structuring guilds...")
    if not converted["worldSaveData"]["value"].get("GroupSaveDataMap"):
        return []
    real_date_time_ticks = converted["worldSaveData"]["value"]["GameTimeSaveData"][
        "value"
    ]["RealDateTimeTicks"]["value"]
    groups = (
        g["value"]["RawData"]["value"]
        for g in converted["worldSaveData"]["value"]["GroupSaveDataMap"]["value"]
        if g["value"]["GroupType"]["value"]["value"] == "EPalGroupType::Guild"
    )
    guilds_generator: GuildGeneratorType = (Guild(g, real_date_time_ticks, filetime).to_dict() for g in groups)
    sorted_guilds: list[Any] = sorted(
        guilds_generator, key=lambda g: g["base_camp_level"], reverse=True
    )
    return list(sorted_guilds)


def main() -> None:
    """NOTE: Requires documentation from the original owner."""
    # pylint: disable-next=C0415
    import time

    start: float = time.time()
    file: str = "./Level.sav"
    converted: dict[str, Any] | str = convert_sav(file)
    if isinstance(converted, str):
        log("Reading json file returned as typeof string", "ERROR")
        sys.exit(1)
    players: list[dict[str, Any]] = structure_player(converted)
    log("Saving players...")
    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4, ensure_ascii=False)
    guilds: list[dict[str, Any]] = structure_guild(converted)
    log("Saving guilds...")
    with open("guilds.json", "w", encoding="utf-8") as f:
        json.dump(guilds, f, indent=4, ensure_ascii=False)
    log(f"Done in {time.time() - start}s")


if __name__ == "__main__":
    main()
