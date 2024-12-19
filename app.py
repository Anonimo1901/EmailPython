import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import json

app = Flask(__name__)


app.config['SECRET_KEY'] = os.urandom(24) 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Cargar datos de config.json
with open('config.json', 'r') as file:
    config = json.load(file)

app.config['MAIL_USERNAME'] = config['remitente']
app.config['MAIL_PASSWORD'] = config['contrasena']

mail = Mail(app)

def cargar_clientes():
    with open('clientes.json', 'r') as file:
        return json.load(file)['clientes']

def guardar_clientes(clientes):
    with open('clientes.json', 'w') as file:
        json.dump({'clientes': clientes}, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    clientes = cargar_clientes()
    mensaje = None
    tipo_mensaje = None

    if 'mensaje' in session:
        mensaje = session['mensaje']
        tipo_mensaje = session['tipo_mensaje']
        session.pop('mensaje', None)
        session.pop('tipo_mensaje', None)

    if request.method == 'POST':
        correos_seleccionados = request.form.getlist('clientes')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')

        if correos_seleccionados:
            enviar_correos(correos_seleccionados, asunto, mensaje)
            session['mensaje'] = 'Correos enviados correctamente.'
            session['tipo_mensaje'] = 'success'
        else:
            session['mensaje'] = 'No se seleccionaron correos.'
            session['tipo_mensaje'] = 'error'

        return redirect(url_for('index'))

    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    correo = request.form['correo']

    clientes = cargar_clientes()

    for cliente in clientes:
        if cliente['correo'] == correo:
            session['mensaje'] = 'Este correo ya está registrado.'
            session['tipo_mensaje'] = 'error'
            return redirect(url_for('index'))

    # Agregar el nuevo cliente
    clientes.append({'nombre': nombre, 'correo': correo})
    guardar_clientes(clientes)
    session['mensaje'] = 'Cliente agregado correctamente.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))

@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    correo = request.form['correo_eliminar']

    clientes = cargar_clientes()

    cliente_a_eliminar = None
    for cliente in clientes:
        if cliente['correo'] == correo:
            cliente_a_eliminar = cliente
            break

    if cliente_a_eliminar:
        clientes.remove(cliente_a_eliminar)
        guardar_clientes(clientes)
        session['mensaje'] = 'Cliente eliminado correctamente.'
        session['tipo_mensaje'] = 'success'
    else:
        session['mensaje'] = 'No se encontró el cliente con ese correo.'
        session['tipo_mensaje'] = 'error'

    return redirect(url_for('index'))

def enviar_correos(correos, asunto, mensaje):
    """ Función para enviar correos a la lista de correos seleccionados """
    for correo in correos:
        msg = Message(asunto,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[correo])
        msg.body = mensaje
        mail.send(msg)

@app.route('/success')
def success():
    return "¡Correos enviados exitosamente!"

if __name__ == "__main__":
    app.run(debug=True)
