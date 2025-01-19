class Subject:

    observadores = []

    def agregar (self, object):
        self.observadores.append (object)

    def quitar (self, object):
        pass

    def notificar (self):
        for observador in self.observadores:
            observador.update()

class PokemonConcreto (Subject):
    def __init__(self):
        self.estado = None
    
    def set_estado (self, value):
        self.estado = value
        self.notificar ()
    
    def get_estado (self, ):
        return self.estado

class Observador:

    def update (self):
        raise NotImplementedError ("Delegación de actualización")
    
class ObservadorConcretoA (Observador):
    def __init__(self, object):
        self.observado_a = object
        self.observado_a.agregar (self)

    def update (self):
        print ("Actualización dentro de Observador ObservadorConcretoA")
        self.estado = self.observado_a.get_estado ()
        print ("Estado = ", self.estado)

tema1 = PokemonConcreto ()

observador_a = ObservadorConcretoA (tema1)
tema1.set_estado (1)

