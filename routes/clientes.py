from flask import render_template, Blueprint, request, session, redirect, url_for
import json
import os

# Creación del Blueprint para manejar las rutas relacionadas con clientes
clientes_bp = Blueprint('clientes', __name__)

# Función para cargar los clientes desde el archivo JSON
def cargar_clientes():
    if os.path.exists('clientes.json'):
        with open('clientes.json', 'r') as file:
            return json.load(file)['clientes']
    else:
        return []

# Función para guardar los clientes en el archivo JSON
def guardar_clientes(clientes):
    with open('clientes.json', 'w') as file:
        json.dump({'clientes': clientes}, file, indent=4)

# Ruta para la página principal que muestra los clientes
@clientes_bp.route('/', methods=['GET'])
def index():
    """Muestra la página principal de clientes."""
    clientes = cargar_clientes()
    mensaje = session.pop('mensaje', None)
    tipo_mensaje = session.pop('tipo_mensaje', None)

    # Renderiza la plantilla 'index.html' con los clientes y los posibles mensajes
    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)


# Ruta para agregar un cliente
@clientes_bp.route('/agregar', methods=['POST'])
def agregar_cliente():
    """Agrega un nuevo cliente."""
    nombre = request.form['nombre']
    correo = request.form['correo']

    # Cargar los clientes existentes
    clientes = cargar_clientes()

    # Verificar si el correo ya está registrado
    for cliente in clientes:
        if cliente['correo'] == correo:
            session['mensaje'] = 'Este correo ya está registrado.'
            session['tipo_mensaje'] = 'error'
            return redirect(url_for('clientes.index'))

    # Agregar el nuevo cliente
    clientes.append({'nombre': nombre, 'correo': correo})
    guardar_clientes(clientes)

    # Mensaje de éxito
    session['mensaje'] = 'Cliente agregado correctamente.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('clientes.index'))

# Ruta para eliminar un cliente
@clientes_bp.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    """Elimina un cliente basado en el correo."""
    correo = request.form['correo_eliminar']

    # Cargar los clientes existentes
    clientes = cargar_clientes()

    # Buscar y eliminar el cliente
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

    return redirect(url_for('clientes.index'))

# Ruta para editar un cliente
@clientes_bp.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    """Edita un cliente (eliminando el anterior y agregando el nuevo)."""
    try:
        nombre = request.form['nombre']
        correo = request.form['correo']
        correo_oculto = request.form['correo_hidden']

        # Cargar los clientes existentes
        clientes = cargar_clientes()

        # Buscar y eliminar el cliente que se va a editar
        cliente_a_eliminar = None
        for cliente in clientes:
            if cliente['correo'] == correo_oculto:
                cliente_a_eliminar = cliente
                break

        if cliente_a_eliminar:
            clientes.remove(cliente_a_eliminar)
        else:
            session['mensaje'] = 'No se encontró el cliente con ese correo.'
            session['tipo_mensaje'] = 'error'
            return redirect(url_for('clientes.index'))

        # Agregar el cliente con los nuevos datos
        clientes.append({'nombre': nombre, 'correo': correo})
        guardar_clientes(clientes)

        # Mensaje de éxito
        session['mensaje'] = 'Cliente editado correctamente.'
        session['tipo_mensaje'] = 'success'

        return redirect(url_for('clientes.index'))

    except KeyError as e:
        session['mensaje'] = 'Error al procesar los datos del formulario.'
        session['tipo_mensaje'] = 'error'
        return redirect(url_for('clientes.index'))
