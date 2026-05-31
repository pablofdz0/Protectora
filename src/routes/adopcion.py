import flask
import flask_login
import sirope
from models.adopcion import Adopcion

blp = flask.Blueprint("adopcion", __name__, url_prefix="/adopcion")
srp = sirope.Sirope()

def str_to_oid(s):
    parts = s.split("@")
    return sirope.OID.from_pair((parts[0], int(parts[1])))

@blp.route("/solicitar/<path:animal_oid>", methods=["GET", "POST"])
@flask_login.login_required
def solicitar(animal_oid):
    animal = srp.load(str_to_oid(animal_oid))
    if flask.request.method == "POST":
        adopcion = Adopcion(
            animal_oid=animal_oid,
            usuario_oid=flask_login.current_user.get_id(),
            notas=flask.request.form["notas"]
        )
        srp.save(adopcion)
        flask.flash("Solicitud de adopción enviada", "success")
        return flask.redirect(flask.url_for("animal.lista"))
    return flask.render_template("adopcion/form.html", animal=animal)

@blp.route("/lista")
@flask_login.login_required
def lista():
    adopciones = Adopcion.find_all(srp)
    resultado = []
    for a in adopciones:
        animal = srp.load(str_to_oid(a.animal_oid))
        resultado.append((a, animal))
    return flask.render_template("adopcion/lista.html", adopciones=resultado)

@blp.route("/gestionar/<path:oid>/<accion>")
@flask_login.login_required
def gestionar(oid, accion):
    adopcion = srp.load(str_to_oid(oid))
    if accion in ("aprobada", "rechazada"):
        adopcion.estado = accion
        if accion == "aprobada":
            animal = srp.load(str_to_oid(adopcion.animal_oid))
            animal.estado = "adoptado"
            srp.save(animal)
        srp.save(adopcion)
        flask.flash(f"Adopción {accion}", "success")
    return flask.redirect(flask.url_for("adopcion.lista"))