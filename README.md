# TBuilder
 *Concept*
 An app that makes creating terraria mods (tmodloader) easier and more intuitive (meant for people who don't
 code)


## How it works:
- Projects are *created* with *1 folder* and *4 files*
    - **Content**: The mod's content, this folder contains pickled (using Python's **pickle** module) files.
    - **description.txt**: The mod's description, this is the same as a regular TModLoader project.
    - **icon.png**: The mod's icon .png, this is the same as a regular TModLoader project.
    - **launch.json**: Information containing launch info, this is the same as Properties/launchSettings.json.
    - **tbuild.json**: Contains information about the project, this is similar to build.txt.
- The editor saves new picked files.
    - The pickled files contains a **Class** representing the object, e.g. *NPC* or *Item*.
- After pressing 'Build' in the 'File' menu, the project is compiled to C#.
    - All pickled files are looped through and the **Class** object is extracted from each and are compiled to
      C#.
    - A **TBuildUtility.cs** file is copied over to the project, a handwritten file for easier C# development.
    - **tbuild.json** is converted to build.txt
    - **launch.json** is put into the Properties/launchSettings.json directory.
    - **description.txt** is copied to the build directory.
    - **icon.png** is copied to the build directory.
