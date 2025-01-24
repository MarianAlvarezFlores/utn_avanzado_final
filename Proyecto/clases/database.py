import sqlite3
from clases.observador import Subject, PokemonCollection

class Database ():

    def __init__(self):
        self.conexion = sqlite3.connect('PokeappDB.db')
        self.cursor = self.conexion.cursor()
    
 
    def create_tables(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pokemon(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    ability TEXT NOT NULL,
                    type TEXT NOT NULL,
                    info TEXT NOT NULL,
                    category TEXT NOT NULL,
                    imagen BLOB NOT NULL
                )
            ''')
        self.conexion.commit()   
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL UNIQUE
                )
            ''')
        self.conexion.commit()

