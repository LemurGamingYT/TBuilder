from dataclasses import dataclass, field


@dataclass
class Drop:
    item_id: int
    minimum_dropped: int = field(default=1)
    maximum_dropped: int = field(default=1)
    chance_denominator: int = field(default=1)
