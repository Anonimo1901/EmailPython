from flask import Flask, render_template, session
from config import Config
from flask_mail import Mail
from routes.clientes import clientes_bp
from routes.correo import correo_bp
from routes.excel_utils import excel_bp

# Inicialización de la aplicación
app = Flask(__name__)

# Configuración de la aplicación
Config.init_app(app)

# Inicializar la extensión Flask-Mail
app.mail = Mail(app)

# Registrar los blueprints
app.register_blueprint(correo_bp, url_prefix='/correo')
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(excel_bp, url_prefix='/excel')

# Ruta principal de la aplicación
@app.route('/')
def index():
    # Suponiendo que la función cargar_clientes está bien definida
    from routes.clientes import cargar_clientes
    clientes = cargar_clientes()

    mensaje = None
    tipo_mensaje = None

    # Manejo de mensajes en sesión
    if 'mensaje' in session:
        mensaje = session['mensaje']
        tipo_mensaje = session['tipo_mensaje']
        session.pop('mensaje', None)
        session.pop('tipo_mensaje', None)

    # Renderizamos la plantilla con los clientes y los mensajes
    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)

if __name__ == '__main__':
    app.run(debug=True)
