from datetime import datetime

class Adopcion:
    def __init__(self, animal_oid, usuario_oid, notas=""):
        self.animal_oid = animal_oid
        self.usuario_oid = usuario_oid
        self.notas = notas
        self.fecha = datetime.now().isoformat()
        self.estado = "pendiente"  # pendiente, aprobada, rechazada

    @staticmethod
    def find_all(srp):
        return list(srp.load_all(Adopcion))

    @staticmethod
    def find_by_usuario(srp, usuario_oid):
        return [a for a in srp.load_all(Adopcion) if a.usuario_oid == usuario_oid]

    @staticmethod
    def find_by_animal(srp, animal_oid):
        return [a for a in srp.load_all(Adopcion) if a.animal_oid == animal_oid]