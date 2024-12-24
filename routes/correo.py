from flask import Blueprint, request, session, redirect, url_for, current_app as app, jsonify
from flask_mail import Message
from routes.clientes import cargar_clientes
import time

correo_bp = Blueprint('correo', __name__)

def enviar_correos(socketio, correos, asunto, mensaje, archivo_imagen=None):
    # Lote de 1 correo y retraso de 5 segundos entre correos
    batch_size = 180
    delay_seconds = 1
    total_correos = len(correos)
    progreso = 0

    for i in range(0, total_correos, batch_size):
        lote = correos[i:i + batch_size]
        
        for j, correo in enumerate(lote):
            msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[correo])
            msg.body = mensaje

            if archivo_imagen:
                msg.attach(archivo_imagen.filename, archivo_imagen.content_type, archivo_imagen.read())

            try:
                app.mail.send(msg)
                print(f"Correo enviado a {correo}")
            except Exception as e:
                print(f"Error enviando correo a {correo}: {str(e)}")

            # Calcular el porcentaje de progreso
            progreso = int(((i + j + 1) / total_correos) * 100)
            socketio.emit('actualizar_progreso', {'progreso': progreso}, namespace='/correo')  # Emitir evento de progreso
            print(f"Progreso: {progreso}%")

            time.sleep(delay_seconds)  # Espera de 1 segundo entre correos

@correo_bp.route('/enviar_correos', methods=['POST'])
def enviar_correos_route():
    asunto = request.form['asunto']
    mensaje = request.form['mensaje']
    correos_seleccionados = request.form.getlist('clientes')
    imagen = request.files.get('imagen')

    clientes = cargar_clientes()

    correos = [cliente['correo'] for cliente in clientes if cliente['correo'] in correos_seleccionados]

    # Aquí asumimos que socketio se pasa correctamente desde el contexto de Flask
    from app import socketio  # Asegúrate de importar socketio correctamente

    if imagen:
        enviar_correos(socketio, correos, asunto, mensaje, imagen)
    else:
        enviar_correos(socketio, correos, asunto, mensaje)

    session['mensaje'] = 'Correos enviados correctamente.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))
