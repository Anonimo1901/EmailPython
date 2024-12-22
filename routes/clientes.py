from flask import render_template, Blueprint, request, session, redirect, url_for, jsonify
import json
import os


clientes_bp = Blueprint('clientes', __name__)


def cargar_clientes():
    if os.path.exists('clientes.json'):
        with open('clientes.json', 'r') as file:
            return json.load(file)['clientes']
    else:
        return []


def guardar_clientes(clientes):
    with open('clientes.json', 'w') as file:
        json.dump({'clientes': clientes}, file, indent=4)


@clientes_bp.route('/', methods=['GET'])
def index():
    """Muestra la página principal de clientes."""
    clientes = cargar_clientes()
    mensaje = session.pop('mensaje', None)
    tipo_mensaje = session.pop('tipo_mensaje', None)


    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)



@clientes_bp.route('/agregar', methods=['POST'])
def agregar_cliente():
    """Agrega un nuevo cliente."""
    nombre = request.form['nombre']
    correo = request.form['correo']


    clientes = cargar_clientes()


    for cliente in clientes:
        if cliente['correo'] == correo:
            session['mensaje'] = 'Este correo ya está registrado.'
            session['tipo_mensaje'] = 'error'
            return redirect(url_for('clientes.index'))


    clientes.append({'nombre': nombre, 'correo': correo})
    guardar_clientes(clientes)


    session['mensaje'] = 'Cliente agregado correctamente.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('clientes.index'))


from flask import jsonify

@clientes_bp.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    try:
        nombre = request.form['nombre']
        correo = request.form['correo']
        correo_oculto = request.form['correo-hidden']

        clientes = cargar_clientes()

        for cliente in clientes:
            if cliente['correo'] == correo_oculto:
                cliente['nombre'] = nombre
                cliente['correo'] = correo
                guardar_clientes(clientes)
                return jsonify({'success': True, 'message': 'Cliente editado correctamente.'})

        return jsonify({'success': False, 'message': 'No se encontró el cliente con ese correo.'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al editar el cliente: {str(e)}'})

@clientes_bp.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    try:
        correo = request.form['correo-hidden']
        clientes = cargar_clientes()

        for cliente in clientes:
            if cliente['correo'] == correo:
                clientes.remove(cliente)
                guardar_clientes(clientes)
                return jsonify({'success': True, 'message': 'Cliente eliminado correctamente.'})

        return jsonify({'success': False, 'message': 'No se encontró el cliente con ese correo.'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al eliminar el cliente: {str(e)}'})

@clientes_bp.route('/eliminar_clientes', methods=['POST'])
def eliminar_clientes():
    try:
        correos_eliminar = request.form.getlist('correos_eliminar')
        clientes = cargar_clientes()
        clientes_eliminados = 0

        for correo in correos_eliminar:
            clientes = [cliente for cliente in clientes if cliente['correo'] != correo]
            clientes_eliminados += 1

        guardar_clientes(clientes)

        if clientes_eliminados > 0:
            return jsonify({'success': True, 'message': f'{clientes_eliminados} cliente(s) eliminado(s) correctamente.'})
        else:
            return jsonify({'success': False, 'message': 'No se encontraron clientes para eliminar.'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al eliminar cliente(s): {str(e)}'})
