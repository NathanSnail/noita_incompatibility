from dataclasses import dataclass, field
import argparse
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
from typing_extensions import List
import math
import os
from itertools import chain
from functools import cmp_to_key
import json


def warn(msg: str):
    print(f"\033[31m[Warning]: \033[0m{msg}")


def fmap[T, U](f: Callable[[T], U], x: Optional[T]) -> Optional[U]:
    return f(x) if x is not None else None


parser = argparse.ArgumentParser(
    prog="detect_incompatibility", description="Detect incompatibilities in Noita mods."
)
parser.add_argument(
    "-w",
    "--workshop",
    help="The path to the workshop mods directory (should end in 881100)",
)
parser.add_argument(
    "-m", "--mods", help="The path to the main mods directory (should end in mods)"
)
parser.add_argument(
    "-c", "--config", help="The path to the config json", default="config.json"
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Print info about what is being done to each file",
    action="store_true",
)
parser.add_argument(
    "-e",
    "--enabled",
    help="Only print incompatibilities in mods that are enabled",
    action="store_true",
)


@dataclass
class Arguments:
    workshop: Optional[Path]
    mods: Optional[Path]
    verbose: bool
    enabled: bool


parsed = parser.parse_args()

config: str = parsed.config
default_config: Dict[str, Any] = json.load(open(config, "r"))
for field in default_config.items():
    if getattr(parsed, field[0]) is None:
        setattr(parsed, field[0], field[1])

print(parsed)


def empty_to_none(value: str) -> Optional[str]:
    if value == "":
        return None
    return value


args = Arguments(
    workshop=fmap(Path, fmap(os.path.expanduser, empty_to_none(parsed.workshop))),
    mods=fmap(Path, fmap(os.path.expanduser, empty_to_none(parsed.mods))),
    verbose=parsed.verbose,
    enabled=parsed.enabled,
)


if args.verbose:
    print(args)


def require_dir(path: Path, suffix: str, kind: str):
    assert path.is_dir(), f"{kind} must be a mods dir, '{path}' isn't"
    if path.name != suffix:
        warn(f"{kind} dir will usually end in {suffix}, '{path}' doesn't")


for path, suffix, kind in [(args.mods, "mods", "Mods")]:
    if path is None:
        continue
    require_dir(path, suffix, kind)
