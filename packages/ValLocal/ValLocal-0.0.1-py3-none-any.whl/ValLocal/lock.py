
from os import getenv
from pathlib import Path

from ValStorage import read_from_drive

from .structs import LockFile

LocalAppData = Path(getenv("LocalAppData", ""))
RiotGames = LocalAppData / "Riot Games"
lockfile = RiotGames / "Riot Client" / "Config" / "lockfile"


def get_lockfile():
    rawText = read_from_drive(lockfile)
    return LockFile(rawText)
