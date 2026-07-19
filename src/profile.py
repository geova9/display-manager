from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from monitor import Monitor
from utilis import load_json, save_json

PROFILE_DIR = Path.home() / ".config" / "display-manager"
PROFILE_FILE = PROFILE_DIR / "profiles.json"


@dataclass
class MonitorProfile:
    name: str
    monitors: List[Monitor] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "monitors": [monitor.as_dict() for monitor in self.monitors],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MonitorProfile":
        monitor_list = [Monitor.from_dict(item) for item in data.get("monitors", [])]
        return cls(name=data.get("name", "unnamed"), monitors=monitor_list)


def load_profiles() -> List[MonitorProfile]:
    raw = load_json(PROFILE_FILE)
    if not raw:
        return []

    profiles = []
    for item in raw:
        try:
            profiles.append(MonitorProfile.from_dict(item))
        except Exception:
            continue
    return profiles


def save_profiles(profiles: List[MonitorProfile]) -> None:
    save_json(PROFILE_FILE, [profile.as_dict() for profile in profiles])


def get_profile(profiles: List[MonitorProfile], name: str) -> Optional[MonitorProfile]:
    for profile in profiles:
        if profile.name == name:
            return profile
    return None
