import flask_login

class Usuario(flask_login.UserMixin):
    def __init__(self, email, password, nombre, rol="cliente"):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.rol = rol  # "cliente" o "veterinario"

    def get_id(self):
        return str(self.__oid__)

    def is_veterinario(self):
        return self.rol == "veterinario"

    @staticmethod
    def find_by_email(srp, email):
        return next((u for u in srp.load_all(Usuario) if u.email == email), None)

    @staticmethod
    def find_all(srp):
        return list(srp.load_all(Usuario))