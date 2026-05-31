import flask
import flask_login
import sirope
from models.usuario import Usuario

blp = flask.Blueprint("auth", __name__, url_prefix="/auth")
srp = sirope.Sirope()

@blp.route("/registro", methods=["GET", "POST"])
def registro():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        nombre = flask.request.form["nombre"]
        rol = flask.request.form["rol"]

        if Usuario.find_by_email(srp, email):
            flask.flash("El email ya está registrado", "error")
            return flask.redirect(flask.url_for("auth.registro"))

        usuario = Usuario(email, password, nombre, rol)
        srp.save(usuario)
        flask.flash("Registro exitoso, inicia sesión", "success")
        return flask.redirect(flask.url_for("auth.login"))

    return flask.render_template("auth/registro.html")

@blp.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]

        usuario = Usuario.find_by_email(srp, email)
        if not usuario or usuario.password != password:
            flask.flash("Credenciales incorrectas", "error")
            return flask.redirect(flask.url_for("auth.login"))

        flask_login.login_user(usuario)
        if usuario.is_veterinario():
            return flask.redirect(flask.url_for("animal.lista"))
        return flask.redirect(flask.url_for("animal.lista"))

    return flask.render_template("auth/login.html")

@blp.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("animal.lista"))