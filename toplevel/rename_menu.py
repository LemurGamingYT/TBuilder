from widgets import TopLevel, Entry, Label, Button


class Rename(TopLevel):
    def __init__(self, master):
        super().__init__(master, fg_color='#011000')
        
        self.title('Rename')
        self.geometry('300x250')
        self.resizable(False, False)
        self.attributes('-topmost', True)
        
        self.new_name = Entry(
            self,
            fg_color='#001c00',
            placeholder_text='New Name',
            font=('Arial', 14)
        )
        self.new_name.place(.5, .75, .75, .25)
        
        Button(
            self,
            text='Rename',
            command=self.destroy,
            fg_color='#001c00',
            hover_color='#011e00',
            font=('Arial', 18, 'bold')
        ).place(.5, .25, .75, .2)
