from customtkinter import (
    CTkButton, CTkLabel, CTkFrame, CTk, CTkToplevel, CTkEntry, CTkScrollableFrame
)

from tkinter import Menu


class Tk(CTk):
    pass

class TopLevel(CTkToplevel):
    pass


class Button(CTkButton):
    def place(self, relx: float, rely: float, relw: float, relh: float, anchor: str = 'c') -> None:
        super().place(relx=relx, rely=rely, relw=relw, relh=relh, anchor=anchor)


class Label(CTkLabel):
    def place(self, relx: float, rely: float, relw: float, relh: float, anchor: str = 'c') -> None:
        super().place(relx=relx, rely=rely, relw=relw, relh=relh, anchor=anchor)


class Frame(CTkFrame):
    def place(self, relx: float, rely: float, relw: float, relh: float, anchor: str = 'c') -> None:
        super().place(relx=relx, rely=rely, relw=relw, relh=relh, anchor=anchor)


class Entry(CTkEntry):
    def place(self, relx: float, rely: float, relw: float, relh: float, anchor: str = 'c') -> None:
        super().place(relx=relx, rely=rely, relw=relw, relh=relh, anchor=anchor)


class ScrollableFrame(CTkScrollableFrame):
    def place(self, relx: float, rely: float, relw: float, relh: float, anchor: str = 'c') -> None:
        super().place(relx=relx, rely=rely, relw=relw, relh=relh, anchor=anchor)
