import flask
import flask_login
import sirope
from models.historial import HistorialMedico

blp = flask.Blueprint("historial", __name__, url_prefix="/historial")
srp = sirope.Sirope()

def str_to_oid(s):
    parts = s.split("@")
    return sirope.OID.from_pair((parts[0], int(parts[1])))

@blp.route("/nuevo/<path:animal_oid>", methods=["GET", "POST"])
@flask_login.login_required
def nuevo(animal_oid):
    animal = srp.load(str_to_oid(animal_oid))
    if flask.request.method == "POST":
        h = HistorialMedico(
            animal_oid=animal_oid,
            descripcion=flask.request.form["descripcion"],
            veterinario=flask.request.form["veterinario"],
            tratamiento=flask.request.form["tratamiento"]
        )
        srp.save(h)
        flask.flash("Entrada médica añadida", "success")
        return flask.redirect(flask.url_for("animal.detalle", oid=animal_oid))
    return flask.render_template("historial/form.html", animal=animal)

@blp.route("/eliminar/<path:oid>/<path:animal_oid>")
@flask_login.login_required
def eliminar(oid, animal_oid):
    srp.delete(srp.load(str_to_oid(oid)))
    flask.flash("Entrada eliminada", "success")
    return flask.redirect(flask.url_for("animal.detalle", oid=animal_oid))