from pickle import loads as ploads, UnpicklingError
from logging import basicConfig, INFO, info, error
from json import dumps, loads
from shutil import copyfile
from pathlib import Path

from classes.zones import Zone
from classes.item import Item
from widgets import TopLevel
from classes.npc import NPC


JSON = {
    'project-name': 'TerraBuilder',
    'project-path': 'C:\\',
    'mod-author': '',
    'mod-version': '0.1',
    'mod-buildIgnore': '*.csproj, *.user, obj/*, bin/*, .vs/*',
    'mod-hideCode': False,
    'mod-hideResources': False
}

LAUNCH_SETTINGS = {
    'profiles': {
        'Terraria': {
            'commandName': 'Executable',
            'executablePath': 'dotnet',
            'commandLineArgs': '$(tMLPath)',
            'workingDirectory': '$(tMLSteamPath)'
        },
        
        'TerrariaServer': {
            'commandName': 'Executable',
            'executablePath': 'dotnet',
            'commandLineArgs': '$(tMLServerPath)',
            'workingDirectory': '$(tMLSteamPath)'
        }
    }
}


def update_json(key: str, json: dict):
    projects_json = Path('./projects.json')
    
    j = {}
    if projects_json.exists():
        j = loads(projects_json.read_text())
    
    j[key] = json
    
    projects_json.write_text(dumps(j, indent=4))


def create_project(path: Path, window: TopLevel) -> dict:
    name = window.name.get()
    project = Path(path / name)
    project.mkdir(exist_ok=True)
    
    json = JSON
    json['project-name'] = name
    json['project-path'] = project.absolute().as_posix()
    
    
    (project / 'Content').mkdir(exist_ok=True)
    
    (project / 'tbuild.json').touch()
    (project / 'launch.json').touch()
    (project / 'description.txt').touch()
    
    (project / 'tbuild.json').write_text(dumps(JSON, indent=4))
    (project / 'launch.json').write_text(dumps(LAUNCH_SETTINGS, indent=4))
    
    copyfile('./assets/default_icon.png', (project / 'icon.png'))
    
    update_json(name, json)
    
    return json


class EditorWriter:
    def __init__(self, editor):
        self.editor = editor
        
        self.project_path: Path = editor.project_path
    
    def save(self, _: Path):
        raise NotImplemented
        # if file.is_file():
        #     obj = ploads(file.read_bytes())
            
        #     for attr in obj.__dict__:
        #         new = obj.__annotations__[attr](getattr(obj, attr))
    
    def _build_build_txt(self, project: Path) -> str:
        tbuild = loads((project / 'tbuild.json').read_text())
        
        return """displayName = {}
author = {}

hideResources = {}
hideCode = {}

buildIgnore = {}

version = {}
""".format(tbuild['project-name'], tbuild['mod-author'], tbuild['mod-hideResources'], tbuild['mod-hideCode'],
           tbuild['mod-buildIgnore'], tbuild['mod-version'])
    
    def build(self):
        build_dir = self.project_path / 'Build'
        build_dir.mkdir(exist_ok=True)
        
        basicConfig(
            filename=(build_dir / 'build.log').absolute().as_posix(),
            encoding='utf-8',
            level=INFO
        )
        
        project = self.project_path
        
        (build_dir / 'Properties').mkdir(exist_ok=True)
        (build_dir / 'Content').mkdir(exist_ok=True)
        
        (build_dir / 'build.txt').touch()
        
        (build_dir / 'build.txt').write_text(self._build_build_txt(project))
        
        self._build_content(project / 'Content', build_dir)
        
        copyfile(project / 'icon.png', build_dir / 'icon.png')
        copyfile(project / 'launch.json', build_dir / 'Properties' / 'launchSettings.json')
        copyfile(project / 'description.txt', build_dir / 'description.txt')
        copyfile('./assets/cs/TBuildUtility.cs', build_dir / 'TBuildUtility.cs')
    
    def _clone_png(self, file: Path, build_dir: Path, obj, cs: Path):
        if file.with_suffix('.png').exists():
            copyfile(file.with_suffix('.png'), build_dir / 'Content' / (file.stem + '.png'))
            info(f'Texture copied for {file.name}')
        else:
            error(f'No texture found for {obj.name}')
        
        info(f'Completed build for Item {cs}')
    
    def generate_npc_text(self, o: NPC):
        text = f"""using Terraria.ModLoader;
using Terraria.ID;
using Terraria;

namespace {o.name}
{{
\tpublic class {o.name} : ModNPC
\t{{"""

        if o.npc_frames > 1:
            text += f"""\t\tpublic override void SetStaticDefaults()
\t\t{{
\t\t\tMain.npcFrameCount[Type] = {o.npc_frames};
\t\t}}"""

        text += f"""\t\tpublic override void SetDefaults()
\t\t{{"""

        if o.copy_npc_id != -1:
            text += f'\n\t\t\tNPC.CloneDefaults({o.copy_npc_id});'

        text += f"""\n\t\t\tNPC.lifeMax = {o.max_life};
\t\t\tNPC.life = {o.life};
\t\t\tNPC.damage = {o.damage};
\t\t\tNPC.defense = {o.defense};
\t\t\tNPC.knockBackResist = {o.knockbackResist}f;
\t\t\tNPC.value = Item.buyPrice({o.value.platinum}, {o.value.gold}, {o.value.silver}, {o.value.copper});
\t\t\tNPC.aiStyle = NPCAIStyleID.{o.ai_style.name};
\t\t}}
\t}}
}}"""

        if o.apply_buff != -1:
            text += f"""\t\tpublic override void ModifyHitPlayer(Player target, ref Player.HurtModifiers modifiers)
\t\t{{
\t\t\ttarget.AddBuff(BuffID.{o.apply_buff.name}, {o.apply_buff_seconds})
\t\t}}
"""

        if o.spawn_biome != Zone.NONE:
            chance = 1.0 if o.spawn_chance == -1 else o.spawn_chance
            text += f"""\t\tpublic override float SpawnChance(NPCSpawnInfo spawnInfo)
\t\t{{
\t\t\treturn spawnInfo.Player.Zone{o.spawn_biome.name} ? {chance}f : 0f
\t\t}}"""

        if o.despawn_outside_biome != Zone.NONE:
            text += f"""\t\tpublic override void PreAI()
\t\t{{
\t\t\tif (NPC.target < 0 || NPC.target == 255 || Main.player[NPC.target].dead || !Main.player[NPC.target].active)
\t\t\t{{
\t\t\t\tNPC.TargetClosest();
\t\t\t}}
\t\t\t
\t\t\tPlayer player = Main.player[npc.target];
\t\t\tif (player.Zone{o.despawn_outside_biome.name})
\t\t\t{{
\t\t\t\tDespawn();
\t\t\t}}
\t\t}}
\t\t
\t\tpublic void Despawn()
\t\t{{
\t\t\tNPC.velocity.y -= .04f;
\t\t\tNPC.EncourageDespawn(10); // Despawn in 10 ticks
\t\t\treturn;
\t\t}}
"""
        
        return text

    def generate_item_class_text(self, o: Item):
        text = f"""using Terraria.ModLoader;
using Terraria.Enums;
using Terraria.ID;
using Terraria;

namespace {o.name}
{{
\tpublic class {o.name} : ModItem
\t{{"""

        if o.sacrifice_count > 1:
            text += f"""\t\tpublic override void SetStaticDefaults()
\t\t{{
\t\t\tItem.ResearchUnlockCount = {o.sacrifice_count};
\t\t}}"""

        damage_type = 'Generic'
        if o.melee:
            damage_type = 'Melee'
        elif o.ranged:
            damage_type = 'Ranged'
        elif o.mage:
            damage_type = 'Magic'
        elif o.summoner:
            damage_type = 'Summon'

        text += f"""\t\tpublic override void SetDefaults()
\t\t{{
\t\t\tItem.width = {o.width};
\t\t\tItem.height = {o.height};
\t\t\tItem.value = Item.buyPrice({o.value.platinum}, {o.value.gold}, {o.value.silver}, {o.value.copper});
\t\t\tItem.SetWeaponValues({o.damage}, {o.knockback}, {o.crit});
\t\t\tItem.rare = ItemRarityID.{o.rarity.name};
\t\t\tItem.DamageType = DamageClass.{damage_type};
\t\t\tItem.accessory = {o.accessory};
\t\t\tItem.maxStack = {o.max_stack};
\t\t\tItem.useTime = {o.use_time};
\t\t\tItem.useAnimation = {o.use_animation};
\t\t\tItem.shoot = {o.shoot_id};
\t\t}}
}}"""
        
        return text
    
    def process_file(self, file: Path, build_dir: Path):
        if file.is_file():
            try:
                o = ploads(file.read_bytes())
            except UnpicklingError:
                error('Failed to build file {}'.format(file))
                return
            
            cs = (build_dir / 'Content' / (file.stem + '.cs'))
            
            if isinstance(o, (NPC, Item)):
                cs.touch()
                if isinstance(o, NPC):
                    cs.write_text(self.generate_npc_text(o))
                elif isinstance(o, Item):
                    cs.write_text(self.generate_item_class_text(o))
                
                self._clone_png(file, build_dir, o, cs)
    
    def _build_content(self, content: Path, build_dir: Path):
        for file in content.iterdir():
            self.process_file(file, build_dir)
