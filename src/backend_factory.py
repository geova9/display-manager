from typing import Dict

from backend import DisplayBackend


def available_backends() -> Dict[str, str]:
    return {
        "hyprland": "Hyprland",
        "caelestia": "Caelestia",
    }


def get_backend_key(label: str) -> str:
    for backend_key, backend_label in available_backends().items():
        if backend_label == label:
            return backend_key
    return label.lower()


def create_backend(name: str) -> DisplayBackend:
    backend_name = name.lower()
    if backend_name == "hyprland":
        from hyprland import HyprlandBackend

        return HyprlandBackend()
    if backend_name == "caelestia":
        from caelestia import CaelestiaBackend

        return CaelestiaBackend()

    raise ValueError(f"Backend '{name}' no soportado")
