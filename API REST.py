from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "llaveultrasecreta"


API_URL = "http://api.example.com/recetas"

@app.route("/")
def home():
    response = requests.get(API_URL)
    if response.status_code == 200:
        recetas = response.json()
    else:
        flash("Error al cargar las recetas desde la API.", "error")
        recetas = []
    return render_template("index.html", recetas=recetas)


@app.route("/receta/<int:receta_id>")
def ver_receta(receta_id):
    response = requests.get(f"{API_URL}/{receta_id}")
    if response.status_code == 200:
        receta = response.json()
        return render_template("detalle.html", receta=receta)
    else:
        flash("Receta no encontrada.", "error")
        return redirect(url_for('home'))


@app.route("/nueva", methods=["GET", "POST"])
def nueva_receta():
    if request.method == "POST":
        nombre = request.form["nombre"]
        ingredientes = request.form["ingredientes"]
        pasos = request.form["pasos"]

        if not nombre or not ingredientes or not pasos:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('nueva_receta'))


        receta = {"nombre": nombre, "ingredientes": ingredientes, "pasos": pasos}
        response = requests.post(API_URL, json=receta)

        if response.status_code == 201:
            flash("Receta agregada exitosamente!", "success")
        else:
            flash("Error al agregar la receta.", "error")
        return redirect(url_for('home'))

    return render_template("nueva.html")


@app.route("/editar/<int:receta_id>", methods=["GET", "POST"])
def editar_receta(receta_id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        ingredientes = request.form["ingredientes"]
        pasos = request.form["pasos"]

        if not nombre or not ingredientes or not pasos:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('editar_receta', receta_id=receta_id))


        receta = {"nombre": nombre, "ingredientes": ingredientes, "pasos": pasos}
        response = requests.put(f"{API_URL}/{receta_id}", json=receta)

        if response.status_code == 200:
            flash("Receta actualizada exitosamente!", "success")
        else:
            flash("Error al actualizar la receta.", "error")
        return redirect(url_for('home'))


    response = requests.get(f"{API_URL}/{receta_id}")
    if response.status_code == 200:
        receta = response.json()
    else:
        flash("Receta no encontrada.", "error")
        return redirect(url_for('home'))
    return render_template("editar.html", receta=receta, receta_id=receta_id)


@app.route("/eliminar/<int:receta_id>")
def eliminar_receta(receta_id):
    response = requests.delete(f"{API_URL}/{receta_id}")
    if response.status_code == 200:
        flash("Receta eliminada exitosamente!", "success")
    else:
        flash("Error al eliminar la receta.", "error")
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
