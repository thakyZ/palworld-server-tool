#!/usr/bin/env python3

"""Main Command Line Module"""

import os
import json
import sys
import time
from typing import Any
from argparse import Namespace, ArgumentParser
from urllib.parse import urljoin
from requests import Response, get as request_get, put as request_put

from .structurer import convert_sav, structure_player, structure_guild
from .logger import log


def main() -> None:
    """Main Command Line Method"""
    output: str | None = None
    start: float = time.time()
    parser = ArgumentParser()
    parser.add_argument("--file", "-f", help="File to convert", type=str, default="Level.sav")
    parser.add_argument("--clear", "-c", help="Clear input file", action="store_true")
    parser.add_argument("--output", "-o", help="Output file", type=str, default="structure.json")
    parser.add_argument("--request", "-r", help="Request", type=str, default="")
    parser.add_argument("--token", "-t", help="Request token", type=str, default="")
    args: Namespace = parser.parse_args()

    if args.request == "":
        output = args.output
        if not args.output.endswith(".json"):
            output = args.output + ".json"

    converted: dict[str, Any] | str = convert_sav(args.file)
    if isinstance(converted, str):
        log("Reading json file returned as typeof string", "ERROR")
        sys.exit(1)
    players: list[Any] = structure_player(converted)
    guilds: list[Any] = structure_guild(converted)

    if args.request == "" and output is not None:
        with open(output, "w", encoding="utf-8") as f:
            json.dump({"players": players, "guilds": guilds}, f, indent=4, ensure_ascii=False)
        log(f"Players: {len(players)}")
        log(f"Guilds: {len(guilds)}")
    else:
        player_url: Any | str = urljoin(args.request, "player")
        guild_url: Any | str = urljoin(args.request, "guild")
        log(f"Put players to {player_url} with Players: {len(players)}")
        player_res: Response = request_get(url=player_url,
                                           headers={"Authorization": f"Bearer {args.token}"},
                                           json=players,
                                           timeout=10)
        if player_res.status_code != 200:
            log(f"Put Players data error: {player_res.text}")

        log(f"Put guilds to {guild_url} with Guilds: {len(guilds)}")
        guild_res: Response = request_put(url=guild_url,
                                          headers={"Authorization": f"Bearer {args.token}"},
                                          json=guilds,
                                          timeout=10)
        if guild_res.status_code != 200:
            log(f"Put Guilds data error: {guild_res.text}")

    try:
        if args.clear is not None:
            os.unlink(args.file)
    except FileNotFoundError:
        pass

    log(f"Done in {round((time.time() - start), 3)}s")


if __name__ == "__main__":
    main()
