from tkinter.filedialog import askdirectory
from pathlib import Path
from json import loads

from customtkinter import set_appearance_mode
set_appearance_mode('dark')

from widgets import Frame, Tk, Button, Label, TopLevel, Entry
from writer import create_project, update_json
from editor import Editor


def error(msg: str, main_win: Tk, x: float = .5, y: float = .65, relwidth: float = 1, relheight: float = .1):
    err_label = Label(
        main_win,
        corner_radius=25,
        fg_color='#011000',
        text_color='#ff0000',
        text=msg,
        font=('Arial', 15, 'bold')
    )
    err_label.configure(text=msg)
    err_label.place(x, y, relwidth, relheight)


def create(p: Path, main_win: Tk):
    if not p.exists():
        p.mkdir()
    
    if not p.is_dir():
        error('Path is not a directory', main_win)
    
    data = create_project(p, main_win)
    
    Editor(main_win.parent, data)


class ImportProject(TopLevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#011000')
        self.parent = parent
        
        self.geometry('200x150')
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.title('Import TBuilder Project')
        
        Button(
            self,
            corner_radius=25,
            fg_color='#011e00',
            hover_color='#032c00',
            text='Import',
            font=('Arial', 15, 'bold'),
            command=self.import_dir
        ).place(.5, .75, .75, .25)
    
    def import_dir(self):
        p = Path(askdirectory(title='Project Path Select', mustexist=True))
        if p.exists():
            data = loads((p / 'tbuild.json').read_text())
            update_json(p.name, data)
            self.destroy()
            Editor(self.parent, data)


class NewProject(TopLevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#011000')
        self.parent = parent
        
        self.geometry('400x350')
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.title('New TBuilder Project')
        
        Label(
            self,
            fg_color='#011000',
            text='New Project',
            font=('Arial', 20, 'bold')
        ).place(.5, .1, 1, .1)
        
        self.name = Entry(
            self,
            corner_radius=25,
            fg_color='#011000',
            font=('Arial', 15, 'bold'),
            placeholder_text='Project Name',
        )
        self.name.place(.5, .25, .5, .1)
        
        self.path = Entry(
            self,
            corner_radius=25,
            fg_color='#011000',
            font=('Arial', 15, 'bold'),
            placeholder_text='Project Path',
        )
        self.path.place(.25, .5, .5, .1)
        
        Button(
            self,
            corner_radius=25,
            fg_color='#011e00',
            hover_color='#032c00',
            text='Browse',
            font=('Arial', 15, 'bold'),
            command=self.browse
        ).place(.75, .5, .5, .1)
        
        Button(
            self,
            corner_radius=25,
            fg_color='#011e00',
            hover_color='#032c00',
            text='Create',
            font=('Arial', 15, 'bold'),
            command=self.create
        ).place(.5, .75, .5, .1)
    
    def create(self):
        create(Path(self.path.get()), self)
    
    def browse(self):
        p = askdirectory(title='Project Path Select', mustexist=True)
        if p != '':
            self.path.delete(0, 'end')
            self.path.insert(0, p)


class App(Tk):
    def __init__(self):
        super().__init__('#011000')
        
        self.title('TBuilder')
        self.geometry('800x600')
        self.resizable(False, False)
        
        projects_json = Path('./projects.json')
        
        self.projects = Frame(
            self,
            fg_color='#011e00'
        )
        self.projects.place(.4, .5, .9, 1)
        
        self.sidebar = Frame(
            self,
            fg_color='#032c00'
        )
        self.sidebar.place(.925, .5, .15, 1)
        
        Button(
            self.sidebar,
            corner_radius=25,
            text='New Project',
            fg_color='#032c00',
            hover_color='#043600',
            font=('Arial', 10, 'bold'),
            command=self.new_project
        ).place(.5, .1, 1, .05)
        
        Button(
            self.sidebar,
            corner_radius=25,
            text='Import Project',
            fg_color='#032c00',
            hover_color='#043600',
            font=('Arial', 10, 'bold'),
            command=self.import_project
        ).place(.5, .2, 1, .05)
        
        if projects_json.exists():
            projects = enumerate(loads(projects_json.read_bytes()).items())
            for i, (name, data) in projects:
                if Path(data['project-path']).absolute().exists():
                    self.make_project_frame(name, data, i)
    
    def new_project(self):
        NewProject(self).mainloop()
    
    def import_project(self):
        ImportProject(self).mainloop()
    
    def make_project_frame(self, name: str, data: dict, y: int):
        project = Frame(
            self.projects,
            fg_color='#032c00',
        )
        project.place(.525, y + .1 * .9, .85, .125)
        
        Label(
            project,
            fg_color='#032c00',
            text=name,
            font=('Arial', 25, 'bold')
        ).place(.5, .15, 1, .25)
        
        Label(
            project,
            fg_color='#032c00',
            text=data['project-path'],
            font=('Arial', 15)
        ).place(.25, .65, .65, .25)
        
        Button(
            project,
            fg_color='#032c00',
            hover_color='#043600',
            text='Open',
            font=('Arial', 15, 'bold'),
            command=lambda: Editor(self, data)
        ).place(.75, .65, .2, .35)


if __name__ == '__main__':
    app = App()
    app.mainloop()
