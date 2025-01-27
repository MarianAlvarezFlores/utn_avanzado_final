class Subject:

    observadores = []

    def agregar (self, object):
        self.observadores.append (object)

    def quitar (self, object):
        pass

    def notificar (self):
        for observador in self.observadores:
            observador.update()

class PokemonCollection (Subject):
    def __init__(self):
        self.estado = None
    
    def set_estado(self, value, notificar=True):
        self.estado = value
        if notificar:
            self.notificar()
    
    def get_estado (self, ):
        return self.estado

class Observador (Subject):

    def update (self):
        raise NotImplementedError ("Delegación de actualización")
    
class ObservadorConcretoAgregar (Observador):
    def __init__(self, object):
        self.observado_agregar = object
        self.observado_agregar.agregar (self)

    def update (self):
        print ("Actualización dentro de Observador ObservadorConcretoAgregar")
        self.estado = self.observado_agregar.get_estado ()
        print ("Estado = ", self.estado)

class ObservadorConcretoModificar (Observador):
    def __init__(self, object):
        self.observado_modificar = object
        self.observado_modificar.agregar (self)

    def update (self):
        print ("Actualización dentro de Observador ObservadorConcretoModificar")
        self.estado = self.observado_modificar.get_estado ()
        print ("Estado = ", self.estado)

class ObservadorConcretoEliminar (Observador):
    def __init__(self, object):
        self.observado_eliminar = object
        self.observado_eliminar.agregar (self)

    def update (self):
        print ("Actualización dentro de Observador ObservadorConcretoEliminar")
        self.estado = self.observado_eliminar.get_estado ()
        print ("Estado = ", self.estado)


tema1 = PokemonCollection ()

observador_a = ObservadorConcretoAgregar (tema1)
tema1.set_estado("Agregamos un pokemon con éxito", notificar=False)

# tema2 = PokemonCollection ()

# observador_b = ObservadorConcretoModificar (tema2)
# tema2.set_estado ("modificamos un pokemon con éxito")

# tema3 = PokemonCollection ()
# observador_c = ObservadorConcretoEliminar (tema3)
# tema3.set_estado ("Eliminamos un pokemon con éxito")

