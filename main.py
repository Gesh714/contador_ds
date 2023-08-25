import tkinter as tk
from modules import gui_module

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('480x360')
        self.gui = gui_module.GUI(self)

if __name__ == '__main__':
    app = App()
    app.mainloop()