from tkinter import Tk, Label, Button, Entry, Frame
from clases.database import Database
from clases.windows import Window

if __name__ == "__main__":
    db = Database()
    db.create_tables()
    
    
    wind = Tk()
    wind.geometry("900x600")
    wind.title("POKÉDEX ©")
    wind.iconbitmap("media/Pokeball.ico")

    app = Window(wind)
    app.widgets()

    
    
    