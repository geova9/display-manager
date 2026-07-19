from dataclasses import dataclass


@dataclass
class Monitor:
    name: str
    active: bool
    primary: bool
    width: int
    height: int
    pos_x: int = 0
    pos_y: int = 0
    scale: float = 1.0
    transform: str = "normal"

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "active": self.active,
            "primary": self.primary,
            "width": self.width,
            "height": self.height,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "scale": self.scale,
            "transform": self.transform,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Monitor":
        return cls(
            name=data.get("name", "unknown"),
            active=data.get("active", False),
            primary=data.get("primary", False),
            width=int(data.get("width", 0)),
            height=int(data.get("height", 0)),
            pos_x=int(data.get("pos_x", 0)),
            pos_y=int(data.get("pos_y", 0)),
            scale=float(data.get("scale", 1.0)),
            transform=str(data.get("transform", "normal")),
        )

    def layout_description(self) -> str:
        return f"{self.name}: {self.width}x{self.height} @ {self.scale} offset ({self.pos_x},{self.pos_y})"
