from json import dumps, loads
from shutil import copyfile
from pathlib import Path

from widgets import TopLevel


JSON = {
    'project-name': 'TerraBuilder',
    'project-path': 'C:\\',
    'mod-author': '',
    'mod-version': '0.1',
    'mod-buildIgnore': '*.csproj, *.user, obj/*, bin/*, .vs/*',
    'mod-hideCode': False,
    'mod-hideResources': False,
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
    copyfile('./assets/cs/TBuildUtility.cs', (project / 'TBuildUtility.cs'))
    
    
    projects_json = Path('./projects.json')
    
    j = {}
    if projects_json.exists():
        j = loads(projects_json.read_text())
    
    j[name] = json
    
    projects_json.write_text(dumps(j, indent=4))
    
    return json
