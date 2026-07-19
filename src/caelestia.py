import json
import subprocess
from typing import List

from backend import DisplayBackend
from monitor import Monitor
from profile import MonitorProfile


class CaelestiaBackend(DisplayBackend):
    def _run(self, args: List[str]) -> str:
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Caelestia command failed: {' '.join(args)}\n{result.stderr.strip()}"
            )
        return result.stdout.strip()

    def list_monitors(self) -> List[Monitor]:
        raw = self._run(["caelestiactl", "monitors", "-j"])
        data = json.loads(raw)
        monitors = []

        for entry in data.get("monitors", []):
            monitors.append(
                Monitor(
                    name=entry.get("id", "unknown"),
                    active=bool(entry.get("connected", False)),
                    primary=bool(entry.get("primary", False)),
                    width=int(entry.get("width", 0)),
                    height=int(entry.get("height", 0)),
                    pos_x=int(entry.get("x", 0)),
                    pos_y=int(entry.get("y", 0)),
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
                "caelestiactl",
                "set-monitor",
                monitor.name,
                f"{monitor.width}x{monitor.height}",
                f"{monitor.pos_x}+{monitor.pos_y}",
                str(monitor.scale),
            ]

            try:
                self._run(command)
            except RuntimeError as exc:
                raise RuntimeError(
                    f"Unable to apply profile '{profile.name}' to monitor '{monitor.name}': {exc}"
                )

        return True
