from datetime import datetime

class Subject: #esto equivale a tema

    observadores = []

    def agregar (self, object):
        self.observadores.append (object)

    def quitar (self, object):
        pass

    def notificar (self, *args):
        for observador in self.observadores:
            observador.update(*args)

class PokemonCollection (Subject):   #esto equivale a tema concreto
    def __init__(self):
        self.estado = None
    
    def set_estado(self, value, notificar=True):
        self.estado = value
        self.hora_estado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if notificar:
            self.notificar()
    
    def get_estado (self ):
        return self.estado
    
    def get_hora_estado(self):  
        return self.hora_estado

class Observador (Subject):

    def update (self, *args):
        raise NotImplementedError ("Delegación de actualización")
    
class ObservadorConcretoAgregar (Observador): #tomar este pbjeto de ejemplo para los demás observadores concretos
    def __init__(self, object):
        self.observado_agregar = object
        self.observado_agregar.agregar (self)

    def update (self, *args):
        print ("Actualización dentro de Observador ObservadorConcretoAgregar", args)
        self.estado = self.observado_agregar.get_estado ()
        self.hora_estado = self.observado_agregar.get_hora_estado()  
        print(f"Estado = {self.estado} | Hora = {self.hora_estado}") 


tema1 = PokemonCollection ()

observador_a = ObservadorConcretoAgregar (tema1)
tema1.set_estado("Se agregó un pokemon con éxito", notificar=False)