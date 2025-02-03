from tkinter import Label, Button, Entry, Frame, filedialog, messagebox
import tkinter.commondialog
from PIL import Image, ImageTk
import base64
from tkinter import ttk
import tkinter
from clases.pokemon import Pokemon, mostrar_mensaje
import io
from functools import wraps
from clases.observador import Subject, PokemonCollection


class Window(Frame, Subject):
    global_image_blob=None

    def init(self, master=None):
        super(master, width=900, height=600)
        self.master = master        
        self.pack()
        self.widgets()
        

    def widgets(self):
        self.button1 = Button(self.master, text="AGREGAR", fg="black", command=self.agregar_pokemon)
        self.button2 = Button(self.master, text="MODIFICAR", fg="black", command=self.modificar_pokemon)
        self.button3 = Button(self.master, text="ELIMINAR", fg="black", command=self.eliminar_pokemon)
        self.button4 = Button(self.master, text="BUSCAR", fg="black", command=self.buscar_pokemon)

        self.button1.place(relx=0.05, rely=0.05, relwidth=0.125, relheight=0.05)
        self.button2.place(relx=0.425, rely=0.05, relwidth=0.125, relheight=0.05)
        self.button3.place(relx=0.825, rely=0.05, relwidth=0.125, relheight=0.05)
        self.button4.place(relx=0.80, rely=0.90, relwidth=0.150, relheight=0.05)

        self.searchbar = ttk.Entry(self.master)
        self.searchbar.place(relx=0.05, rely=0.90, relwidth=0.75, relheight=0.05)

        frame_tree = Frame(self.master)
        frame_tree.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.75)

        scroll_y = ttk.Scrollbar(frame_tree, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(frame_tree, 
                                columns=("Nombre", "Tipo 1", "Tipo 2", "Categoría", "Habilidad", "Info"), 
                                show="headings",
                                yscrollcommand=scroll_y.set
                                )

        scroll_y.config(command=self.tree.yview)

        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo 1", text="Tipo 1")
        self.tree.heading("Tipo 2", text="Tipo 2")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Habilidad", text="Habilidad")
        self.tree.heading("Info", text="Info")
        self.tree.column("Nombre", width=100)
        self.tree.column("Tipo 1", width=100)
        self.tree.column("Tipo 2", width=150)
        self.tree.column("Categoría", width=100)
        self.tree.column("Habilidad", width=100)
        self.tree.column("Info", width=100)
        self.tree.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.75)
        self.load_grid() 
        self.mainloop()
        
    def agregar_pokemon(self):
        pokemon = Pokemon()
        types = pokemon.get_types()
        new_window = tkinter.Toplevel(self.master)
        new_window.title("Agregar Pokémon")
        new_window.geometry("350x450")
        new_window.iconbitmap("media/Pokeball.ico")
        entry_nombre = tkinter.Entry(new_window)
        entry_nombre.grid(row=1, column=1, padx=10, pady=5)
        entry_numero = tkinter.Entry(new_window)
        entry_numero.grid(row=2, column=1, padx=10, pady=5)
        entry_category = tkinter.Entry(new_window)
        entry_category.grid(row=3, column=1, padx=10, pady=5)
        entry_info = tkinter.Entry(new_window)
        entry_info.grid(row=4, column=1, padx=10, pady=5)
        entry_type = ttk.Combobox(new_window,values=types,state='readonly')
        entry_type.grid(row=5, column=1, padx=10, pady=5)
        entry_type2 = ttk.Combobox(new_window,values=types,state='readonly')
        entry_type2.grid(row=6, column=1, padx=10, pady=5)
        entry_ability = tkinter.Entry(new_window)
        entry_ability.grid(row=7, column=1, padx=10, pady=5)
        
        button_image = tkinter.Button(new_window,text='Cargar imagen',command = lambda: self.guardar_imagen_en_bd(new_window))
        button_image.grid(row=8,column=1,padx=10,pady=5)
        
        label_nombre = tkinter.Label(new_window, text="Nombre:")
        label_nombre.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        label_numero = tkinter.Label(new_window, text="Número:")
        label_numero.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        label_category = tkinter.Label(new_window, text="Categoría:")
        label_category.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        label_info = tkinter.Label(new_window, text="Información:")
        label_info.grid(row=4, column=0, sticky="e", padx=10, pady=5)
        label_type = tkinter.Label(new_window, text="Tipo 1:")
        label_type.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        label_type2 = tkinter.Label(new_window, text="Tipo 2:")
        label_type2.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        label_ability = tkinter.Label(new_window, text="Habilidad:")
        label_ability.grid(row=7, column=0, sticky="e", padx=10, pady=5)
        label_imagen = tkinter.Label(new_window, text="Imagen:")
        label_imagen.grid(row=8, column=0, sticky="e", padx=10, pady=5)
        
        button_image =  tkinter.Button(new_window,text='Guardar',command=lambda:(pokemon.agregar_pokemon(
            entry_nombre.get().strip(),
            entry_numero.get().strip(), 
            entry_type.get().strip(),
            entry_type2.get().strip(),
            entry_info.get().strip(), 
            entry_category.get().strip(),
            entry_ability.get().strip(),
            self.global_image_blob),
            new_window.destroy()))
        button_image.grid(row=9,column=1,padx=10,pady=5)

        self.load_grid() 

        
    def cargar_imagen(self):
        """Función para cargar una imagen y convertirla en base64"""
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if file_path:
            with open(file_path, "rb") as image_file:
                image_bytes = image_file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            self.global_image_blob= image_base64
            return image_base64

    def guardar_imagen_en_bd(self,new_window):
        """Simular el guardado del valor base64 en una base de datos"""
        imagen_base64 = self.cargar_imagen()
        if imagen_base64:
            self.cargar_imagen_desde_base64(imagen_base64,new_window)
            

    def cargar_imagen_desde_base64(self, base64_string,new_window,label_imagen=None):
        try:
            if base64_string:
                image_bytes = base64.b64decode(base64_string)
                image = Image.open(io.BytesIO(image_bytes))
                image.thumbnail((150,150))
                image_tk = ImageTk.PhotoImage(image)
                show_image=''
                if label_imagen:
                    label_imagen.config(image=image_tk)
                    label_imagen.image = image_tk 
                    label_imagen.grid(row=11, column=0, sticky=("N","W"), padx=550)
                else:
                    show_image = tkinter.Label(new_window)
                    show_image.grid(row=7, column=1, sticky="e", padx=10, pady=5)
                    show_image.config(image = image_tk)
                    show_image.image = image_tk
                    new_window.lift()
        except:
            print('No existe imagen.')

    def eliminar_pokemon(self):
        pokemon = Pokemon() 
        new_window = tkinter.Toplevel(self.master)
        new_window.title("Eliminar Pokémon")
        new_window.geometry("280x150")
        new_window.iconbitmap("media/Pokeball.ico")

        label_nombre = tkinter.Label(new_window, text="Nombre del Pokémon:")
        label_nombre.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        entry_nombre = tkinter.Entry(new_window)
        entry_nombre.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

        button_eliminar = tkinter.Button(
            new_window, 
            text="Eliminar", 
            command=lambda: (
                pokemon.eliminar_pokemon(entry_nombre.get().strip()), 
                new_window.destroy()
            )
        )
        button_eliminar.grid(row=3, column=0, columnspan=2, pady=10)

        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_columnconfigure(1, weight=1)

    def load_grid(self):
        pokemon = Pokemon()
        pokemons = pokemon.get_pokemons()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for poke in pokemons:
            self.tree.insert("", "end", values=poke)

    @mostrar_mensaje (tipo = "error", titulo = "Advertencia" ) 
    def modificar_pokemon(self):
        pokemon = Pokemon()
        types = pokemon.get_types()
        selected_item = self.tree.selection()
        if not selected_item:
            return {"mensaje": "Por favor selecciona un Pokémon"}

        data_grid = self.tree.item(selected_item[0], "values")
        pokemon_data = pokemon.buscar_pokemon_por_nombre(data_grid[0])
        if not data_grid:
            messagebox.showerror("Error", "No se pudo obtener la información del Pokémon.")
            return
        #print(pokemon_data[0])
        new_window = tkinter.Toplevel(self.master)
        new_window.title("Modificar Pokémon")
        new_window.geometry("340x450")
        new_window.iconbitmap("media/Pokeball.ico")

        entry_nombre = tkinter.Entry(new_window)
        entry_nombre.grid(row=1, column=2, padx=10, pady=5)
        entry_nombre.insert(0, pokemon_data[1])
        entry_numero = tkinter.Entry(new_window)
        entry_numero.grid(row=2, column=2, padx=10, pady=5)
        entry_numero.insert(0, pokemon_data[2])
        entry_ability = tkinter.Entry(new_window)
        entry_ability.grid(row=3, column=2, padx=10, pady=5)
        entry_ability.insert(0, pokemon_data[3])
        entry_type = ttk.Combobox(new_window, values=types, state='readonly')
        entry_type.grid(row=4, column=2, padx=10, pady=5)
        entry_type.set(pokemon_data[4])
        entry_type2 = ttk.Combobox(new_window, values=types, state='readonly')
        entry_type2.grid(row=5, column=2, padx=10, pady=5)
        entry_type2.set(pokemon_data[5])
        entry_info = tkinter.Entry(new_window)
        entry_info.grid(row=6, column=2, padx=10, pady=5)
        entry_info.insert(0, pokemon_data[6])
        entry_category = tkinter.Entry(new_window)
        entry_category.grid(row=7, column=2, padx=10, pady=5)
        entry_category.insert(0, pokemon_data[7])

        label_nombre = tkinter.Label(new_window, text="Nombre:")
        label_nombre.grid(row=1, column=1, padx=10, pady=5)
        label_numero = tkinter.Label(new_window, text="Número:")
        label_numero.grid(row=2, column=1, padx=10, pady=5)
        label_ability = tkinter.Label(new_window, text="Habilidad:")
        label_ability.grid(row=3, column=1, padx=10, pady=5)
        label_type = tkinter.Label(new_window, text="Tipo 1:")
        label_type.grid(row=4, column=1, padx=10, pady=5)
        label_type2 = tkinter.Label(new_window, text="Tipo 2:")
        label_type2.grid(row=5, column=1, padx=10, pady=5)
        label_info = tkinter.Label(new_window, text="Información:")
        label_info.grid(row=6, column=1, padx=10, pady=5)
        label_category = tkinter.Label(new_window, text="Categoría:")
        label_category.grid(row=7, column=1, padx=10, pady=5)       

        button_image = tkinter.Button(new_window, text='Cargar imagen', command=lambda: self.guardar_imagen_en_bd(new_window))
        button_image.grid(row=8, column=1, columnspan=2, padx=15, pady=5)

        def guardar_cambios():
            if not hasattr(self, "global_image_blob") or self.global_image_blob is None:
                self.global_image_blob = pokemon_data[8]

            pokemon.modificar_pokemon(
                entry_nombre.get().strip(),
                entry_numero.get().strip(),
                entry_ability.get().strip(),
                entry_type.get().strip(),
                entry_type2.get().strip(),
                entry_info.get().strip(),
                entry_category.get().strip(),
                self.global_image_blob
            )
            new_window.destroy()
            self.load_grid()

        button_save = tkinter.Button(new_window, text='Guardar', command=lambda: guardar_cambios())
        button_save.grid(row=9, column=1, columnspan=2, padx=15, pady=5)

    @mostrar_mensaje (tipo = "error", titulo = "Advertencia" ) 
    def buscar_pokemon(self):
        nombre_pokemon = self.searchbar.get().strip()
        if not nombre_pokemon:
            return {"mensaje": "Por favor, ingresa el nombre de un Pokémon para buscar"}

        pokemon = Pokemon()
        resultado = pokemon.buscar_pokemon_por_nombre(nombre_pokemon)

        if not resultado:
            return {"mensaje": f"No se encontró ningún Pokémon llamado '{nombre_pokemon}'"}

        new_window = tkinter.Toplevel(self.master)
        new_window.title(f"Detalles de {resultado[1]}")
        new_window.geometry("700x400")

        etiquetas = ["ID", "NOMBRE", "NUMERO", "HABILIDAD", "TIPO 1", "TIPO 2", "INFO", "CATEGORÍA"]
        for i, detalle in enumerate(resultado[:-1]):
            label = tkinter.Label(new_window, text=f"{etiquetas[i]}: {detalle}")
            label.pack(anchor="w", padx=10, pady=5)

        if resultado[-1]:
            try:
                image_bytes = base64.b64decode(resultado[-1])
                image = Image.open(io.BytesIO(image_bytes))
                image.thumbnail((150, 150))
                image_tk = ImageTk.PhotoImage(image)
                image_label = tkinter.Label(new_window, image=image_tk)
                image_label.image = image_tk
                image_label.pack(pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")