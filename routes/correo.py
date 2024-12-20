from flask import Blueprint, request, session, redirect, url_for, current_app as app
from flask_mail import Message
from routes.clientes import cargar_clientes

correo_bp = Blueprint('correo', __name__)

def enviar_correos(correos, asunto, mensaje, archivo_imagen=None):
    for correo in correos:
        msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[correo])
        msg.body = mensaje

        if archivo_imagen:
            msg.attach(archivo_imagen.filename, archivo_imagen.content_type, archivo_imagen.read())

        try:
            app.mail.send(msg)
        except Exception as e:
            print(f"Error enviando correo a {correo}: {str(e)}")

@correo_bp.route('/enviar_correos', methods=['POST'])
def enviar_correos_route():
    asunto = request.form['asunto']
    mensaje = request.form['mensaje']
    correos_seleccionados = request.form.getlist('clientes')
    imagen = request.files.get('imagen')

    clientes = cargar_clientes()

    correos = [cliente['correo'] for cliente in clientes if cliente['correo'] in correos_seleccionados]


    if imagen:
        enviar_correos(correos, asunto, mensaje, imagen)
    else:
        enviar_correos(correos, asunto, mensaje)

    session['mensaje'] = 'Correos enviados correctamente.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))
