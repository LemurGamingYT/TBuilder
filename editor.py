from pickle import loads, dumps, UnpicklingError
from contextlib import suppress
from subprocess import Popen
from tkinter import Event
from pathlib import Path
from enum import Enum

from widgets import Tk, Label, ScrollableFrame, Menu, Button, Entry, CheckBox, OptionMenu
from assets.utils.names import display_name
from toplevel.rename_menu import Rename
from classes.value import Value
from writer import EditorWriter
from classes.item import Item
from classes.npc import NPC


class Editor:
    def __init__(self, tk: Tk, data: dict):
        self.data = data
        self.tk = tk
        
        self.selected_content = None
        
        self.project_path = Path(data['project-path'])
        
        self.writer = EditorWriter(self)
        
        
        tk.state('zoomed')
        tk.resizable(False, False)
        tk.title('TBuilder - Editor')
        
        for widget in tk.winfo_children():
            widget.destroy()
        
        topbar = Menu(tk, tearoff=0, fg='#001c00')
        
        filemenu = Menu(topbar, tearoff=0)
        filemenu.add_command(label='Save', command=lambda: self.save(self.selected_content))
        filemenu.add_command(label='Build', command=self.writer.build)
        
        adding_menu = Menu(tk, tearoff=0)
        adding_menu.add_command(label='Add NPC', command=self.add_npc)
        adding_menu.add_command(label='Add Item', command=self.add_item)
        
        topbar.add_cascade(label='File', menu=filemenu)
        topbar.add_cascade(label='Add', menu=adding_menu)
        
        self.tk.configure(menu=topbar)
        
        self.right_click_item = Menu(tk, tearoff=0)
        self.right_click_item.add_command(label='Open in File Manager', command=self.open_content)
        self.right_click_item.add_command(label='Delete', command=self.delete_content)
        self.right_click_item.add_command(label='Rename', command=self.rename_content)
        
        self.content = ScrollableFrame(
            tk,
            fg_color='#011e00'
        )
        self.content.place(.1, .5, .25, 1)
        
        self.properties = ScrollableFrame(
            tk,
            fg_color='#011e00'
        )
        self.properties.place(.65, .5, .75, 1)
        
        Label(
            self.content,
            fg_color='#011e00',
            text='Mod Content',
            font=('Arial', 20, 'bold')
        ).pack(fill='x')
        
        self.load_mod_content()
    
    def delete_content(self):
        if self.selected_content is None:
            return
        
        self.selected_content.unlink()
        self.load_mod_content()
    
    def rename_content(self):
        if self.selected_content is None:
            return
        
        def on_close():
            with suppress(FileExistsError):
                self.selected_content.rename(self.selected_content.parent / rename.new_name.get())
                
            rename.destroy()
            
            self.load_mod_content()
        
        rename = Rename(self.tk)
        
        rename.protocol('WM_DELETE_WINDOW', on_close)
        
        rename.mainloop()
    
    def open_content(self):
        if self.selected_content is None:
            return
        
        Popen(f'explorer /select,"{self.selected_content.absolute().as_posix()}"')
    
    def save(self, file: Path):
        self.writer.save(file)
    
    def add_right_click_menu(self, event: Event):
        try:
            self.right_click_item.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_item.grab_release()
    
    def load_mod_content(self, path: Path = None):
        if path is None:
            path = self.project_path
        
        for widget in self.content.winfo_children():
            if not isinstance(widget, Label):
                widget.destroy()
        
        mod_content = (path / 'Content').iterdir()
        for content in mod_content:
            if content.is_dir():
                continue
            
            try:
                o = loads(content.read_bytes())
            except UnpicklingError:
                continue
            
            btn = Button(
                self.content,
                corner_radius=25,
                fg_color='#011e00',
                hover_color='#032c00',
                text=o.name + ': ' + o.__class__.__name__,
                font=('Arial', 15, 'bold')
            )
            
            btn.configure(command=lambda obj=o: self.open_properties(obj, content))
            btn.bind('<Button-3>', self.add_right_click_menu)
            
            btn.pack(fill='x')
    
    def add_npc(self):
        npc = NPC()
        npc.name = 'NewNPC'
        
        (self.project_path / 'Content' / 'NewNPC').write_bytes(dumps(npc))
        self.load_mod_content(self.project_path)
    
    def add_item(self):
        item = Item()
        item.name = 'NewItem'
        
        (self.project_path / 'Content' / 'NewItem').write_bytes(dumps(item))
        self.load_mod_content(self.project_path)
    
    def open_properties(self, cls, content: Path):
        for widget in self.properties.winfo_children():
            widget.destroy()
        
        self.selected_content = content
        
        values = zip(cls.__annotations__.values(), cls.__dict__.items())
        for y, (annotation, (attr_name, attr_value)) in enumerate(values):
            self.make_property(annotation, attr_name, attr_value, y)
    
    default_entry_properties = {'fg_color': '#011e00', 'font': ('Courier New', 15)}
    default_label_properties = {'fg_color': '#011e00', 'font': ('Arial', 20, 'bold')}
    default_checkbox_properties = {'fg_color': '#011e00', 'font': ('Courier New', 20, 'bold')}
    default_optionmenu_properties = {'fg_color': '#011e00'}
    def make_property(self, annotation: type, attr_name: str, attr_value, y: int) -> None:
        display = display_name(attr_name)
        if annotation is str:
            Label(
                self.properties,
                text=display,
                **self.default_label_properties
            ).grid(row=y, column=0)
            
            e = Entry(
                self.properties,
                placeholder_text=display,
                **self.default_entry_properties
            )
            e.insert(0, attr_value)
            e.grid(row=y, column=1)
        elif annotation is int:
            Label(
                self.properties,
                text=display,
                **self.default_label_properties
            ).grid(row=y, column=0)
            
            e = Entry(
                self.properties,
                placeholder_text=display,
                **self.default_entry_properties
            )
            e.insert(0, str(attr_value))
            e.grid(row=y, column=1)
        elif annotation is float:
            Label(
                self.properties,
                text=display,
                **self.default_label_properties
            ).grid(row=y, column=0)
            
            e = Entry(
                self.properties,
                placeholder_text=display,
                **self.default_entry_properties
            )
            e.insert(0, str(attr_value))
            e.grid(row=y, column=1)
        elif annotation is bool:
            CheckBox(
                self.properties,
                text=display,
                **self.default_checkbox_properties
            ).grid(row=y, column=0, sticky='w')
        elif issubclass(annotation, Enum):
            Label(
                self.properties,
                text=display,
                **self.default_label_properties
            ).grid(row=y, column=0)
            
            OptionMenu(
                self.properties,
                values=[
                    attr
                    for attr in dir(attr_value)
                    if attr not in {'name', 'value'} and not attr.startswith('__')
                ],
                **self.default_optionmenu_properties
            ).grid(row=y, column=1)
        elif annotation is Value:
            Label(
                self.properties,
                text=display,
                **self.default_label_properties
            ).grid(row=y, column=0)
            
            plat = Entry(
                self.properties,
                placeholder_text='Platinum',
                **self.default_entry_properties
            )
            plat.insert(0, str(attr_value.platinum))
            plat.grid(row=y, column=1)
            
            gold = Entry(
                self.properties,
                placeholder_text='Gold',
                **self.default_entry_properties
            )
            gold.insert(0, str(attr_value.gold))
            gold.grid(row=y, column=2)
            
            silver = Entry(
                self.properties,
                placeholder_text='Silver',
                **self.default_entry_properties
            )
            silver.insert(0, str(attr_value.silver))
            silver.grid(row=y, column=3)
            
            copper = Entry(
                self.properties,
                placeholder_text='Copper',
                **self.default_entry_properties
            )
            copper.insert(0, str(attr_value.copper))
            copper.grid(row=y, column=4)
