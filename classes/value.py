from dataclasses import dataclass, field


@dataclass
class Value:
    platinum: int = field(default=0)
    gold: int = field(default=0)
    silver: int = field(default=0)
    copper: int = field(default=0)
