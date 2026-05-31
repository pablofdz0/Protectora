from datetime import datetime

class HistorialMedico:
    def __init__(self, animal_oid, descripcion, veterinario, tratamiento=""):
        self.animal_oid = animal_oid
        self.descripcion = descripcion
        self.veterinario = veterinario
        self.tratamiento = tratamiento
        self.fecha = datetime.now().isoformat()

    @staticmethod
    def find_by_animal(srp, animal_oid):
        return [h for h in srp.load_all(HistorialMedico) if h.animal_oid == animal_oid]