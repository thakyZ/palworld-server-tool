#!/usr/bin/env python3

"""World Types Module"""

from typing import Any, Literal
from uuid import UUID
from .logger import log
from .pal_skills import PalSkills
from .pal_type import PalType


def hex_uuid_to_decimal(uuid: str | UUID | Any) -> str:
    """Converts a HEX UUID to decimal place.

    Args:
        uuid (str | UUID | Any): The instance of a UUID or string of a UUID.

    Returns:
        str: The decimal representation of the UUID in decimal.
    """
    if not isinstance(uuid, str) and not isinstance(uuid, UUID):
        uuid = str(uuid)
    if isinstance(uuid, str):
        hex_part: str = uuid.split("-")[0]
        decimal_number = int(hex_part, 16)
        return str(decimal_number)
    return str(uuid.int)


# pylint: disable-next=R0902,R0903
class Player:
    """Class containing player data."""

    def __init__(self, uid: str, data: dict[str, Any]) -> None:
        self.player_uid: str = hex_uuid_to_decimal(uid)
        self.nickname: str = data["NickName"]["value"] if data.get("NickName") else ""
        self.level: float | int = (
            int(data["Level"]["value"]) if data.get("Level") else 1
        )
        self.exp: float | int = int(data["Exp"]["value"]) if data.get("Exp") else 0
        self.hp: float | int = (
            int(data["HP"]["value"]["Value"]["value"]) if data.get("HP") else 0
        )
        self.max_hp: float | int = (
            int(data["MaxHP"]["value"]["Value"]["value"]) if data.get("MaxHP") else 0
        )
        self.shield_hp: float | int = (
            int(data["ShieldHP"]["value"]["Value"]["value"])
            if data.get("ShieldHP")
            else 0
        )
        self.shield_max_hp: float | int = (
            int(data["ShieldMaxHP"]["value"]["Value"]["value"])
            if data.get("ShieldMaxHP")
            else 0
        )
        self.max_status_point: float | int = (
            int(data["MaxSP"]["value"]["Value"]["value"]) if data.get("MaxSP") else 0
        )
        self.status_point: dict[str, Any] = {
            s["StatusName"]["value"]: s["StatusPoint"]["value"]
            for s in data["GotStatusPointList"]["value"]["values"]
        }
        full_stomach: float | int = (
            float(data["FullStomach"]["value"]) if data.get("FullStomach") else 0
        )
        self.full_stomach: float | int = round(full_stomach, 2)
        self.pals: list[dict[str, Any]] = []

        self.__order: list[str] = [
            "player_uid",
            "nickname",
            "level",
            "exp",
            "hp",
            "max_hp",
            "shield_hp",
            "shield_max_hp",
            "max_status_point",
            "status_point",
            "full_stomach",
            "pals",
        ]

    def to_dict(self) -> dict[str, Any]:
        """Converts itself to a dictionary.

        Returns:
            dict[str, Any]: The keys and values of all properties in this class.
        """
        return {
            attr: getattr(self, attr)
            for attr in self.__order
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }


# pylint: disable-next=R0902,R0903
class Pal:
    """Class containing pal data."""
    def __init__(self, data: dict[str, Any]) -> None:
        self.owner: str = hex_uuid_to_decimal(data["OwnerPlayerUId"]["value"])
        # self.nickname = data["Nickname"]["value"] if data.get("Nicknme") else ""
        self.level: int = int(data["Level"]["value"]) if data.get("Level") else 1
        self.exp: int = int(data["Exp"]["value"]) if data.get("Exp") else 0
        self.hp: int = (
            int(data["HP"]["value"]["Value"]["value"]) if data.get("HP") else 0
        )
        self.max_hp: int = (
            int(data["MaxHP"]["value"]["Value"]["value"]) if data.get("MaxHP") else 0
        )
        self.gender: str = (
            data["Gender"]["value"]["value"].split("::")[-1]
            if data.get("Gender")
            else "Unknow"
        )
        self.is_lucky: bool | Literal[False] = (
            data["IsRarePal"]["value"] if data.get("IsRarePal") else False
        )
        self.is_boss: bool | Literal[False] = False

        if data.get("CharacterID"):
            typename: str = data["CharacterID"]["value"]
            typename_upper: str = typename.upper()
            if typename_upper[:5] == "BOSS_":
                typename_upper = typename_upper.replace("BOSS_", "")
                self.is_boss = not self.is_lucky
            self.is_tower: bool = typename_upper.startswith("GYM_")
            self.type: str = PalType.get(typename_upper, typename)
        else:
            self.is_tower = False
            self.type = "Unknow"
        self.workspeed: float | int = (
            data["CraftSpeed"]["value"] if data.get("CraftSpeed") else 0
        )
        self.melee: int = (
            int(data["Talent_Melee"]["value"]) if data.get("Talent_Melee") else 0
        )
        self.ranged: int = (
            int(data["Talent_Shot"]["value"]) if data.get("Talent_Shot") else 0
        )
        self.defense: int = (
            int(data["Talent_Defense"]["value"]) if data.get("Talent_Defense") else 0
        )
        self.rank: int = int(data["Rank"]["value"]) if data.get("Rank") else 1
        self.skills: list[str] = (
            self.trans_skill(data["PassiveSkillList"]["value"]["values"])
            if data.get("PassiveSkillList")
            else []
        )

        self.__order: list[str] = [
            "owner",
            # "nickname",
            "level",
            "exp",
            "hp",
            "max_hp",
            "type",
            "gender",
            "is_lucky",
            "is_boss",
            "is_tower",
            "workspeed",
            "melee",
            "ranged",
            "defense",
            "rank",
            "skills",
        ]

    def trans_skill(self, skill_values: list[str]) -> list[str]:
        """Transfers the skills from the `PalSkills` enum that match that which are in the parameter
           `skill_values` and returns them as a string of list.

        Args:
            skill_values (list[str]): The value of skills to gra from the `PalSkills` enum.

        Returns:
            list[str]: The skills that match the argument.
        """
        skills: list[str] = []
        for skill in skill_values:
            if skill in PalSkills.__members__:
                skills.append(PalSkills[skill].value)
            else:
                skills.append(skill)
                log(f"Unknown skill {skill}", "WARN")
        return skills

    def to_dict(self) -> dict[str, Any]:
        """Converts itself to a dictionary.

        Returns:
            dict[str, Any]: The keys and values of all properties in this class.
        """
        return {
            attr: getattr(self, attr)
            for attr in self.__order
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }


class Guild:
    """Class containing guild data."""
    def __init__(self, data: dict[str, Any]) -> None:
        self.name: str = data["guild_name"]
        self.base_camp_level: int = data["base_camp_level"]
        self.admin_player_uid: str = hex_uuid_to_decimal(data["admin_player_uid"])
        self.players: list[dict[str, Any]] = [
            {
                "player_uid": hex_uuid_to_decimal(player["player_uid"]),
                "nickname": player["player_info"]["player_name"],
            }
            for player in data["players"]
        ]
        self.base_ids: list[str] = [str(x) for x in data["base_ids"]]
        self.__order: list[str] = [
            "name",
            "base_camp_level",
            "admin_player_uid",
            "players",
            "base_ids",
        ]

    def to_dict(self) -> dict[str, Any]:
        """Converts itself to a dictionary.

        Returns:
            dict[str, Any]: The keys and values of all properties in this class.
        """
        return {
            attr: getattr(self, attr)
            for attr in self.__order
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }
