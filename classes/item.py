from dataclasses import dataclass, field

from .rarity_id import RarityID
from .sound_id import SoundID
from .value import Value


@dataclass
class Item:
    crit: int = field(default=0)
    width: int = field(default=0)
    height: int = field(default=0)
    damage: int = field(default=0)
    defense: int = field(default=0)
    ammo_id: int = field(default=-1)
    shoot_id: int = field(default=0)
    max_stack: int = field(default=0)
    use_time: int = field(default=100)
    use_animation: int = field(default=100)
    sacrifice_count: int = field(default=1)
    
    mage: bool = field(default=False)
    melee: bool = field(default=False)
    ranged: bool = field(default=False)
    summoner: bool = field(default=False)
    accessory: bool = field(default=False)
    
    knockback: float = field(default=0.0)
    
    value: Value = field(default_factory=Value)
    
    use_sound: SoundID = field(default=SoundID.ITEM1)    
    
    rarity: RarityID = field(default=RarityID.WHITE)
