import os
import json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración del correo (si decides usarlo)
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

# Cargar los clientes desde el archivo JSON
def cargar_clientes():
    if os.path.exists('clientes.json'):
        with open('clientes.json', 'r') as file:
            return json.load(file)['clientes']
    else:
        return []

# Guardar los clientes en el archivo JSON
def guardar_clientes(clientes):
    with open('clientes.json', 'w') as file:
        json.dump({'clientes': clientes}, file, indent=4)

# Ruta principal
@app.route('/')
def index():
    clientes = cargar_clientes()
    mensaje = None
    tipo_mensaje = None

    if 'mensaje' in session:
        mensaje = session['mensaje']
        tipo_mensaje = session['tipo_mensaje']
        session.pop('mensaje', None)
        session.pop('tipo_mensaje', None)

    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)

# Ruta para agregar clientes desde un archivo Excel
@app.route('/agregar_clientes_excel', methods=['POST'])
def agregar_clientes_excel():
    archivo = request.files['archivo']
    columna_nombre = request.form['columna_nombre']
    columna_email = request.form['columna_email']
    
    # Leer el archivo Excel usando pandas
    df = pd.read_excel(archivo)
    clientes = cargar_clientes()

    # Agregar los nuevos clientes
    for _, row in df.iterrows():
        cliente = {
            "nombre": row[columna_nombre],
            "correo": row[columna_email]
        }
        clientes.append(cliente)

    guardar_clientes(clientes)
    
    session['mensaje'] = 'Clientes agregados correctamente desde Excel.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))

# Ruta para agregar un cliente manualmente
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
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

# Ruta para eliminar un cliente
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

# Ruta para editar un cliente
@app.route('/editar_cliente', methods=['POST'])
def editar_cliente():
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
        session['mensaje'] = 'Error al procesar los datos del formulario.'
        session['tipo_mensaje'] = 'error'
        return redirect(url_for('index'))

# Función para enviar correos (opcional)
def enviar_correos(correos, asunto, mensaje):
    for correo in correos:
        msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[correo])
        msg.body = mensaje
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error enviando correo a {correo}: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
