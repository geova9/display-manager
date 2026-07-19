import json
import subprocess
from typing import List

from backend import DisplayBackend
from monitor import Monitor
from profile import MonitorProfile


class HyprlandBackend(DisplayBackend):
    def _run(self, args: List[str]) -> str:
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Hyprland command failed: {' '.join(args)}\n{result.stderr.strip()}"
            )
        return result.stdout.strip()

    def list_monitors(self) -> List[Monitor]:
        raw = self._run(["hyprctl", "monitors", "-j"])
        data = json.loads(raw)
        monitors = []

        for entry in data.get("monitors", []):
            resolution = entry.get("resolution", {})
            offset = entry.get("offset", {})
            monitors.append(
                Monitor(
                    name=entry.get("name", "unknown"),
                    active=bool(entry.get("active", False)),
                    primary=bool(entry.get("primary", False)),
                    width=int(resolution.get("width", 0)),
                    height=int(resolution.get("height", 0)),
                    pos_x=int(offset.get("x", 0)),
                    pos_y=int(offset.get("y", 0)),
                    scale=float(entry.get("scale", 1.0)),
                    transform=str(entry.get("transform", "normal")),
                )
            )

        return monitors

    def apply_profile(self, profile: MonitorProfile) -> bool:
        for monitor in profile.monitors:
            if not monitor.active:
                continue

            command = [
                "hyprctl",
                "dispatch",
                "setmonitor",
                monitor.name,
                f"{monitor.width}x{monitor.height}",
                f"{monitor.pos_x}x{monitor.pos_y}",
                str(monitor.scale),
            ]

            try:
                self._run(command)
            except RuntimeError as exc:
                raise RuntimeError(
                    f"Unable to apply profile '{profile.name}' to monitor '{monitor.name}': {exc}"
                )

        return True
