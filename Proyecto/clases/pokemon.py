from clases.database import Database
from tkinter import messagebox, filedialog, PhotoImage
import re
import functools
from functools import wraps

def mostrar_mensaje(tipo, titulo):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultado = func(*args, **kwargs)
            if resultado and "mensaje" in resultado:
                mensaje = resultado["mensaje"]
                if tipo == "info":
                    messagebox.showinfo(titulo, mensaje)
                elif tipo == "error":
                    messagebox.showerror(titulo, mensaje)
            return resultado
        return wrapper
    return decorador

class Pokemon:
    types = ['Agua', 'Planta', 'Eléctrico', 'Fantasma', 'Normal', 'Fuego', 'Tierra',
             'Hada', 'Dragón', 'Veneno', 'Acero', 'Siniestro', 'Roca', 'Bicho',
             'Volador', 'Psíquico', 'Lucha', 'Hielo']
    
    def __init__(self):
        super().__init__() 

    def get_types(self):
        return self.types

    @mostrar_mensaje("info", "¡ÉXITO!")
    def agregar_pokemon(self, nombre, numero, tipo, tipo2, info, category, ability, global_image_blob):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
            return {"mensaje": "El nombre sólo puede tener letras y espacios. Intentá de nuevo, por favor."}
        if len(info) == 0 or len(category) == 0 or len(ability) == 0:
            return {"mensaje": "Rellená todos los campos correctamente."}

        database.cursor.execute("SELECT id FROM pokemon WHERE nombre = ?", (nombre,))
        pokemon_existe = database.cursor.fetchone()

        if pokemon_existe:
            database.cursor.execute(''' 
                UPDATE pokemon 
                SET numero = ?, type = ?, type2 = ?, info = ?, category = ?, ability = ?, imagen = ? 
                WHERE nombre = ? 
            ''', (numero, tipo, tipo2, info, category, ability, global_image_blob, nombre))
            database.conexion.commit()
            return {"mensaje": f"{nombre} modificado correctamente en la Pokédex."}
        else:
            database.cursor.execute(''' 
                INSERT INTO pokemon (nombre, numero, type, type2, info, category, ability, imagen) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
            ''', (nombre, numero, tipo, tipo2, info, category, ability, global_image_blob))
            database.conexion.commit()
            return {"mensaje": f"Añadiste a {nombre} correctamente."}
        
    def get_pokemons(self):
        database = Database()

        database.cursor.execute("SELECT nombre, type, type2, category, ability, info FROM pokemon")
        pokemons = database.cursor.fetchall()
        return pokemons
    
    @mostrar_mensaje(tipo="info", titulo="Resultado de la operación")
    def eliminar_pokemon(self, nombre):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
            return {"mensaje": f"El nombre sólo puede tener letras y espacios. Intentá de nuevo."}
        
        database.cursor.execute("SELECT id FROM pokemon WHERE nombre = ?", (nombre,))
        pokemon_existe = database.cursor.fetchone()

        if pokemon_existe:
            database.cursor.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))
            database.conexion.commit()
            return {"mensaje": f"El Pokémon {nombre} fue eliminado exitosamente de la Pokédex."}
        else:
            return {"mensaje": f"El Pokémon {nombre} no existe en la Pokédex."}

    @mostrar_mensaje(tipo="info", titulo="Resultado de la modificación")
    def modificar_pokemon(self, nombre, numero, tipo, tipo2, info, categoria, habilidad, global_image_blob):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
           return {"mensaje": f"El nombre sólo puede tener letras y espacios. Intentá de nuevo."}

        if len(info) == 0 or len(categoria) == 0 or len(habilidad) == 0:
            return {"mensaje": f"Rellená todos los campos correctamente."}

        database.cursor.execute("SELECT id FROM pokemon WHERE nombre = ?", (nombre,))
        pokemon_existe = database.cursor.fetchone()

        if pokemon_existe:
            database.cursor.execute('''
                UPDATE pokemon
                SET numero = ?, type = ?, type2 = ?, info = ?, category = ?, ability = ?, imagen = ?
                WHERE nombre = ?
            ''', (numero, tipo, tipo2, info, categoria, habilidad, global_image_blob, nombre))
            database.conexion.commit()
            return {"mensaje": f"{nombre} fue modificado correctamente."}
        else:
            return {"mensaje": f"El Pokémon {nombre} no existe en la Pokédex."}

    @mostrar_mensaje(tipo="info", titulo="Error")
    def buscar_pokemon_por_nombre(self, nombre):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
            messagebox.showerror("ERROR", "El nombre sólo puede tener letras y espacios. Intentá de nuevo.")
            return None

        query = "SELECT * FROM pokemon WHERE nombre = ?"
        database.cursor.execute(query, (nombre,))
        return database.cursor.fetchone()
