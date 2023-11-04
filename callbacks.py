from contextlib import suppress

from widgets import Entry


def clone(widget):
    parent = widget.nametowidget(widget.winfo_parent())
    cls = widget.__class__
    
    clone = cls(parent)
    for key in widget.__dict__['_tclCommands']:
        with suppress(ValueError):
            clone.configure({key: widget.cget(key)})
    
    return clone


entry_callback = lambda cls, e, data_name, **_: e.insert(0, cls.__dict__[data_name.lower().replace(' ', '_')])

def create_value_field(cls, e: Entry, data_name: str, *, x: int, y: int, **kwargs):
    value = cls.__dict__[data_name.lower()]
    
    e.insert(0, str(value.platinum))
    
    gold = clone(e)
    gold.insert(0, str(value.gold))
    gold.grid(row=y, column=x + 2)
    
    silver = clone(e)
    silver.insert(0, str(value.silver))
    silver.grid(row=y, column=x + 3)
    
    copper = clone(e)
    copper.insert(0, str(value.copper))
    copper.grid(row=y, column=x + 4)
