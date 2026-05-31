import flask
import flask_login
import sirope

app = flask.Flask(__name__)
app.secret_key = "protectora_secret_key"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

srp = sirope.Sirope()

@app.errorhandler(403)
def forbidden(e):
    return flask.render_template("403.html"), 403

@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html"), 404

@app.route("/")
def index():
    return flask.render_template("index.html")

from routes import auth, animal, historial, adopcion

app.register_blueprint(auth.blp)
app.register_blueprint(animal.blp)
app.register_blueprint(historial.blp)
app.register_blueprint(adopcion.blp)

@login_manager.user_loader
def user_loader(uid):
    parts = uid.split("@")
    oid = sirope.OID.from_pair((parts[0], int(parts[1])))
    return srp.load(oid)

if __name__ == "__main__":
    app.run(debug=True)