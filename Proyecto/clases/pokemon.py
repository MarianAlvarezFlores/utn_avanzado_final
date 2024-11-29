from clases.database import Database
from tkinter import messagebox, filedialog, PhotoImage
import re

class Pokemon:
    types = ['Agua','Planta','Eléctrico','Fantasma','Normal','Fuego','Tierra', 'Hada','Dragón', 'Veneno', 'Acero', 'Siniestro', 'Roca', 'Bicho', 'Volador', 'Psíquico', 'Lucha', 'Hielo']
            
    
    def get_types(self):
        return self.types
    
    def agregar_pokemon(self,nombre,numero,type,type2,info,category,ability,global_image_blob):
        database = Database()
    
        if not re.match (r"^[A-Za-z\s]+$", nombre):
            messagebox.showerror("¡OOPS!", "El nombre sólo puede tener letras y espacios. Intentá de nuevo, por favor.")
            return
        if len (info) == 0 or len (category) == 0 or len (ability) == 0:
            messagebox.showerror("¡OOPS!", "Rellená todos los campos correctamente.")
            return

        database.cursor.execute ("SELECT id FROM pokemon WHERE nombre = ?", (nombre,))
        pokemon_existe = database.cursor.fetchone ()

        if pokemon_existe:
            database.cursor.execute ('''
                UPDATE pokemon
                SET numero = ?, type = ?, type2 = ? info = ?, category = ?, ability = ?, imagen = ?
                WHERE nombre = ?
            ''', (numero, type, type2, info, category, ability, global_image_blob, nombre))
            messagebox.showinfo("¡ÉXITO!", f"{nombre} agregado correctamente a la Pokédex.")
        else:
            database.cursor.execute ('''
                INSERT INTO pokemon (nombre, numero, type, type2, info, category, ability, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, numero, type, type2, info, category, ability, global_image_blob))
            messagebox.showinfo ("¡ÉXITO!", f"Añadiste a {nombre} correctamente.")

        database.conexion.commit ()
        
    def get_pokemons(self):
        database = Database()

        database.cursor.execute("SELECT nombre, type, type2, category, ability, info FROM pokemon")
        pokemons = database.cursor.fetchall()
        return pokemons
    
    def eliminar_pokemon(self, nombre):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
            messagebox.showerror("Error", "El nombre sólo puede tener letras y espacios. Intentá de nuevo.")
            return

        database.cursor.execute("SELECT id FROM pokemon WHERE nombre = ?", (nombre,))
        pokemon_existe = database.cursor.fetchone()

        if pokemon_existe:
            database.cursor.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))
            database.conexion.commit()
            messagebox.showinfo("MODIFICACIÓN EXITOSA", f"El Pokémon {nombre} fue eliminado exitosamente de la Pokédex.")
        else:
            messagebox.showerror("NO ENCONTRADO", f"El Pokémon {nombre} no existe en la Pokédex.")

    def modificar_pokemon(self, nombre, numero, tipo, tipo2, info, categoria, habilidad, global_image_blob):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
            messagebox.showerror("Error", "El nombre sólo puede tener letras y espacios. Intentá de nuevo.")
            return

        if len(info) == 0 or len(categoria) == 0 or len(habilidad) == 0:
            messagebox.showerror("ERROR", "Rellená todos los campos correctamente.")
            return

        database.cursor.execute("SELECT id FROM pokemon WHERE nombre = ?", (nombre,))
        pokemon_existe = database.cursor.fetchone()

        if pokemon_existe:
            database.cursor.execute('''
                UPDATE pokemon
                SET numero = ?, type = ?, type2 = ?, info = ?, category = ?, ability = ?, imagen = ?
                WHERE nombre = ?
            ''', (numero, tipo, tipo2, info, categoria, habilidad, global_image_blob, nombre))
            database.conexion.commit()
            messagebox.showinfo("¡Éxito!", f"{nombre} fue modificado correctamente.")
        else:
            messagebox.showerror("ERROR", f"El Pokémon {nombre} no existe en la Pokédex.")

    def buscar_pokemon_por_nombre(self, nombre):
        database = Database()

        if not re.match(r"^[A-Za-z\s]+$", nombre):
            messagebox.showerror("ERROR", "El nombre sólo puede tener letras y espacios. Intentá de nuevo.")
            return None

        query = "SELECT * FROM pokemon WHERE nombre = ?"
        database.cursor.execute(query, (nombre,))
        return database.cursor.fetchone()
