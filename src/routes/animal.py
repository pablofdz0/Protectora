import flask
import flask_login
import sirope
import os
from werkzeug.utils import secure_filename
from models.animal import Animal

blp = flask.Blueprint("animal", __name__, url_prefix="/animal")
srp = sirope.Sirope()

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../static/fotos")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def str_to_oid(s):
    parts = s.split("@")
    return sirope.OID.from_pair((parts[0], int(parts[1])))

@blp.route("/")
def lista():
    animales = Animal.find_all(srp)
    return flask.render_template("animal/lista.html", animales=animales)

@blp.route("/nuevo", methods=["GET", "POST"])
@flask_login.login_required
def nuevo():
    if not flask_login.current_user.is_veterinario():
        flask.abort(403)
    if flask.request.method == "POST":
        foto = None
        file = flask.request.files.get("foto")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            foto = filename

        animal = Animal(
            nombre=flask.request.form["nombre"],
            especie=flask.request.form["especie"],
            raza=flask.request.form["raza"],
            edad=flask.request.form["edad"],
            descripcion=flask.request.form["descripcion"],
            foto=foto
        )
        srp.save(animal)
        flask.flash("Animal añadido correctamente", "success")
        return flask.redirect(flask.url_for("animal.lista"))
    return flask.render_template("animal/form.html", animal=None)

@blp.route("/editar/<path:oid>", methods=["GET", "POST"])
@flask_login.login_required
def editar(oid):
    if not flask_login.current_user.is_veterinario():
        flask.abort(403)
    animal = srp.load(str_to_oid(oid))
    if flask.request.method == "POST":
        animal.nombre = flask.request.form["nombre"]
        animal.especie = flask.request.form["especie"]
        animal.raza = flask.request.form["raza"]
        animal.edad = flask.request.form["edad"]
        animal.descripcion = flask.request.form["descripcion"]
        animal.estado = flask.request.form["estado"]
        file = flask.request.files.get("foto")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            animal.foto = filename
        srp.save(animal)
        flask.flash("Animal actualizado", "success")
        return flask.redirect(flask.url_for("animal.lista"))
    return flask.render_template("animal/form.html", animal=animal)

@blp.route("/eliminar/<path:oid>")
@flask_login.login_required
def eliminar(oid):
    if not flask_login.current_user.is_veterinario():
        flask.abort(403)
    from models.historial import HistorialMedico
    from models.adopcion import Adopcion
    oid_obj = str_to_oid(oid)
    for h in HistorialMedico.find_by_animal(srp, oid):
        srp.delete(h.__oid__)
    for a in Adopcion.find_by_animal(srp, oid):
        srp.delete(a.__oid__)
    srp.delete(oid_obj)
    flask.flash("Animal eliminado", "success")
    return flask.redirect(flask.url_for("animal.lista"))

@blp.route("/detalle/<path:oid>")
def detalle(oid):
    from models.historial import HistorialMedico
    from models.adopcion import Adopcion
    animal = srp.load(str_to_oid(oid))
    historial = HistorialMedico.find_by_animal(srp, oid)
    adopciones = Adopcion.find_by_animal(srp, oid)
    return flask.render_template("animal/detalle.html", animal=animal, historial=historial, adopciones=adopciones)