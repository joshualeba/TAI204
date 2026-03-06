from flask import Flask, render_template, request, redirect # Herramientas para crear el sitio web (Flask)
import requests # Librería para mandar peticiones a nuestra API de FastAPI

app = Flask(__name__) # Iniciamos nuestra aplicación web

# Dirección (URL) donde está corriendo nuestra API de FastAPI
url = "http://127.0.0.1:5000/v1/usuarios/"

# Página principal: muesta la lista de usuarios
@app.route('/')
def inicio():
    req = requests.get(url) # Le pedimos a la API la lista de usuarios
    datos = req.json() # Convertimos la respuesta en un formato que Python entienda
    usuarios = datos.get("Usuarios", []) # Sacamos solo la lista de la bolsa de datos
    return render_template('index.html', usuarios=usuarios) # Mandamos los datos a la página HTML

# Ruta para recibir los datos del formulario y mandarlos a la API
@app.route('/guardar', methods=['POST'])
def guardar():
    # Armamos el paquete de datos con lo que el usuario escribió en la web
    datos = {
        "id": int(request.form['id']), # El id se saca del formulario
        "nombre": request.form['nombre'], # El nombre se saca del formulario
        "edad": request.form['edad'] # La edad se saca del formulario
    }
    requests.post(url, json=datos) # Mandamos el paquete a la API usando POST
    return redirect('/') # Regresamos a la página principal para ver el cambio

# Ruta para borrar un usuario dándole su ID
@app.route('/borrar/<id>')
def borrar(id):
    requests.delete(url + id) # Le pedimos a la API que borre ese ID usando DELETE
    return redirect('/') # Regresamos a la página principal

# Si ejecutamos este archivo directamente, se prende el servidor web
if __name__ == '__main__':
    app.run(debug=True, port=8000) # El sitio web corre en el puerto 8000