from datetime import datetime

class Animal:
    def __init__(self, nombre, especie, raza, edad, descripcion, estado="disponible", foto=None):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.descripcion = descripcion
        self.estado = estado
        self.foto = foto  # nombre del archivo
        self.fecha_entrada = datetime.now().isoformat()

    @staticmethod
    def find_all(srp):
        return list(srp.load_all(Animal))

    @staticmethod
    def find_by_oid(srp, oid):
        return srp.load(oid)