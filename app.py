import os
import webbrowser  # Para abrir el navegador automáticamente
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Cargar las credenciales del correo desde un archivo de configuración
with open('config.json', 'r') as file:
    config = json.load(file)

app.config['MAIL_USERNAME'] = config['remitente']
app.config['MAIL_PASSWORD'] = config['contrasena']

mail = Mail(app)

def cargar_clientes():
    """ Cargar los clientes desde el archivo JSON. """
    with open('clientes.json', 'r') as file:
        return json.load(file)['clientes']

def guardar_clientes(clientes):
    """ Guardar la lista de clientes en el archivo JSON. """
    with open('clientes.json', 'w') as file:
        json.dump({'clientes': clientes}, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Mostrar la lista de clientes y enviar correos. """
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
    """ Agregar un nuevo cliente. """
    nombre = request.form['nombre']
    correo = request.form['correo']

    clientes = cargar_clientes()

    # Verificar si el correo ya está registrado
    for cliente in clientes:
        if cliente['correo'] == correo:
            session['mensaje'] = 'Este correo ya está registrado.'
            session['tipo_mensaje'] = 'error'
            return redirect(url_for('index'))

    clientes.append({'nombre': nombre, 'correo': correo})
    guardar_clientes(clientes)
    session['mensaje'] = 'Cliente agregado correctamente.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))

@app.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    """ Eliminar un cliente. """
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

@app.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    """ Editar un cliente: eliminar y agregar con los datos modificados. """
    try:
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        correo_oculto = request.form['correo_hidden']  # Campo oculto con el correo original

        # Cargar los clientes
        clientes = cargar_clientes()

        # Eliminar el cliente con el correo original
        cliente_a_eliminar = None
        for cliente in clientes:
            if cliente['correo'] == correo_oculto:
                cliente_a_eliminar = cliente
                break

        if cliente_a_eliminar:
            clientes.remove(cliente_a_eliminar)  # Eliminamos el cliente
            print(f"Cliente eliminado: {cliente_a_eliminar}")  # Confirmación de eliminación
        else:
            session['mensaje'] = 'No se encontró el cliente con ese correo.'
            session['tipo_mensaje'] = 'error'
            return redirect(url_for('index'))

        # Agregar el cliente con los nuevos datos
        clientes.append({'nombre': nombre, 'correo': correo})
        guardar_clientes(clientes)  # Guardamos los cambios en el archivo JSON

        session['mensaje'] = 'Cliente editado correctamente (eliminado y agregado).'
        session['tipo_mensaje'] = 'success'

        return redirect(url_for('index'))

    except KeyError as e:
        print(f"Error al obtener datos del formulario: {e}")
        session['mensaje'] = 'Error al procesar los datos del formulario.'
        session['tipo_mensaje'] = 'error'
        return redirect(url_for('index'))

def enviar_correos(correos, asunto, mensaje):
    """ Función para enviar correos a la lista de correos seleccionados. """
    for correo in correos:
        msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[correo])
        msg.body = mensaje
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error enviando correo a {correo}: {str(e)}")

if __name__ == '__main__':
    # Abrir automáticamente el navegador
    webbrowser.open("http://127.0.0.1:5000/")  # URL predeterminada de Flask

    # Iniciar la aplicación Flask
    app.run(debug=True)
