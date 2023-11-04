from pickle import loads, dumps
from tkinter import Event
from pathlib import Path

from widgets import Tk, Label, ScrollableFrame, Menu, Button, Entry
from classes.npc import NPC


class Editor:
    def __init__(self, tk: Tk, data: dict):
        self.data = data
        self.tk = tk
        
        tk.state('zoomed')
        tk.resizable(False, False)
        tk.title('TBuilder - Editor')
        
        for widget in tk.winfo_children():
            widget.destroy()
        
        self.adding_menu = Menu(tk, tearoff=0)
        self.adding_menu.add_command(label='Add NPC', command=self.add_npc)
        self.adding_menu.add_command(label='Add Item')
        self.adding_menu.add_command(label='Add Tile')
        
        self.content = ScrollableFrame(
            tk,
            fg_color='#011e00'
        )
        self.content.place(.1, .5, .25, 1)
        
        self.properties = ScrollableFrame(
            tk,
            fg_color='#011e00',
            orientation='horizontal'
        )
        self.properties.place(.65, .5, .75, 1)
        
        Label(
            self.content,
            fg_color='#011e00',
            text='Mod Content',
            font=('Arial', 20, 'bold')
        ).pack(fill='x')
        
        self.project_path = Path(data['project-path'])
        self.load_mod_content(self.project_path)
        
        tk.bind('<Button-3>', self.adding_menu_popup)
    
    def adding_menu_popup(self, event: Event):
        try:
            self.adding_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.adding_menu.grab_release()
    
    def load_mod_content(self, path: Path):
        mod_content = (path / 'Content').iterdir()
        for content in mod_content:
            if content.is_dir():
                continue
            
            o = loads(content.read_bytes())
            btn = Button(
                self.content,
                corner_radius=25,
                fg_color='#011e00',
                hover_color='#032c00',
                text=o.name + ': ' + o.__class__.__name__,
                font=('Arial', 15, 'bold')
            )
            
            btn.configure(command=lambda obj=o: self.open_properties(obj))
            
            btn.pack(fill='x')
    
    def add_npc(self):
        npc = NPC()
        npc.name = 'NewNPC'
        
        (self.project_path / 'Content' / 'NewNPC').write_bytes(dumps(npc))
        self.load_mod_content(self.project_path)
    
    def open_properties(self, cls: NPC):
        if isinstance(cls, NPC):
            Label(
                self.properties,
                fg_color='#011e00',
                text='Name',
                font=('Arial', 20, 'bold')
            ).place(.1, .05, .2, .05)
            
            name = Entry(
                self.properties,
                fg_color='#011e00',
                font=('Arial', 15, 'bold'),
                placeholder_text='Name'
            )
            name.insert(0, cls.name)
            name.place(.1, .1, .2, .05)
