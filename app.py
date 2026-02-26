from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<div>your fake name <input type="text"/></div><div>choisis une partie du code à maquiller<select><option>header</option><option>body</option></select></div><div>choisis un maquillage<select><option>paupieres</option><option>rouge a levres</option></select></div><div>choisis une couleur<input type="color"/></div>"
