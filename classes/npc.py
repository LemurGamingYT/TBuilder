from dataclasses import dataclass, field

from .sound_id import SoundID
from .zones import Zone
from .drop import Drop


@dataclass
class NPC:
    name: str = field(default='')
    
    life: int = field(default=0)
    width: int = field(default=0)
    value: int = field(default=0)
    alpha: int = field(default=0)
    height: int = field(default=0)
    damage: int = field(default=0)
    defense: int = field(default=0)
    max_life: int = field(default=0)
    ai_style: int = field(default=-1)
    npc_frames: int = field(default=1)
    apply_buff: int = field(default=-1)
    must_be_day: int = field(default=-1)
    copy_npc_id: int = field(default=-1)
    
    boss: bool = field(default=False)
    no_gravity: bool = field(default=False)
    has_downed: bool = field(default=False)
    no_tile_collide: bool = field(default=False)
    
    npc_slots: float = field(default=1.0)
    knockbackResist: float = field(default=0.0)
    
    drops: list[Drop] = field(default_factory=list)
    
    hit_sound: SoundID = field(default=SoundID.NPCHIT1)
    death_sound: SoundID = field(default=SoundID.NPCDEATH1)
    
    spawn_biome: Zone = field(default=Zone.NONE)
