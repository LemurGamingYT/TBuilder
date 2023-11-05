from dataclasses import dataclass, field

from .ai_style_id import AIStyleID
from .sound_id import SoundID
from .buff_id import BuffID
from .value import Value
from .zones import Zone
from .drop import Drop


@dataclass
class NPC:
    name: str = field(default='')
    
    life: int = field(default=0)
    width: int = field(default=0)
    alpha: int = field(default=0)
    height: int = field(default=0)
    damage: int = field(default=0)
    defense: int = field(default=0)
    max_life: int = field(default=0)
    npc_frames: int = field(default=1)
    must_be_day: int = field(default=-1)
    copy_npc_id: int = field(default=-1)
    spawn_chance: int = field(default=-1)
    apply_buff_seconds: int = field(default=0)
    
    boss: bool = field(default=False)
    no_gravity: bool = field(default=False)
    has_downed: bool = field(default=False)
    no_tile_collide: bool = field(default=False)
    
    npc_slots: float = field(default=1.0)
    knockbackResist: float = field(default=0.0)
    
    drops: list[Drop] = field(default_factory=list)
    
    apply_buff: BuffID = field(default=-1)
    value: Value = field(default_factory=Value)
    spawn_biome: Zone = field(default=Zone.NONE)
    hit_sound: SoundID = field(default=SoundID.NPCHIT1)
    ai_style: AIStyleID = field(default=AIStyleID.PASSIVE)
    despawn_outside_biome: Zone = field(default=Zone.NONE)
    death_sound: SoundID = field(default=SoundID.NPCDEATH1)
