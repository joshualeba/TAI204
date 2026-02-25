from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

url = "http://127.0.0.1:5000/v1/usuarios/"

@app.route('/')
def inicio():
    req = requests.get(url)
    datos = req.json()
    usuarios = datos.get("Usuarios", [])
    return render_template('index.html', usuarios=usuarios)

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = {
        "id": int(request.form['id']),
        "nombre": request.form['nombre'],
        "edad": request.form['edad']
    }
    requests.post(url, json=datos)
    return redirect('/')

@app.route('/borrar/<id>')
def borrar(id):
    requests.delete(url + id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)