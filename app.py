import webbrowser
from flask import Flask, render_template, session
from config import Config
from flask_mail import Mail
from flask_socketio import SocketIO  # Importa SocketIO
from routes.clientes import clientes_bp
from routes.correo import correo_bp
from routes.excel_utils import excel_bp

app = Flask(__name__)

# Inicializa la configuración
Config.init_app(app)

# Inicializa Flask-Mail
app.mail = Mail(app)

# Inicializa SocketIO
socketio = SocketIO(app)  # Aquí está la inicialización de SocketIO

# Registra los Blueprints
app.register_blueprint(correo_bp, url_prefix='/correo')
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(excel_bp, url_prefix='/excel')

@app.route('/')
def index():
    print("Ruta / accedida")  # Imprime cuando accedes a la ruta '/'
    
    from routes.clientes import cargar_clientes
    clientes = cargar_clientes()

    mensaje = None
    tipo_mensaje = None

    if 'mensaje' in session:
        mensaje = session['mensaje']
        tipo_mensaje = session['tipo_mensaje']
        session.pop('mensaje', None)
        session.pop('tipo_mensaje', None)

    print(f"Clientes cargados: {len(clientes)}")  # Muestra cuántos clientes se cargaron
    
    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)

@app.route('/p')
def base():
    print("Ruta /p accedida")  # Imprime cuando accedes a la ruta '/p'
    return render_template('base.html')

# Esta función es un ejemplo de cómo podrías emitir progreso a través de SocketIO
def emitir_progreso():
    for i in range(1, 101):  # Simula un progreso del 1% al 100%
        print(f"Emitiendo progreso: {i}%")  # Muestra el progreso
        socketio.emit('actualizar_progreso', {'progreso': i})
        socketio.sleep(0.1)  # Simula un pequeño delay entre cada emisión

if __name__ == '__main__':
    print("Iniciando servidor con SocketIO...")  # Imprime cuando el servidor comienza

    # Abrir el navegador en la URL 127.0.0.1:5000
    webbrowser.open("http://127.0.0.1:5000")

    # Ejecutar el servidor Flask sin mostrar la consola (ocultamos la consola en Windows con pythonw)
    socketio.run(app, debug=True, use_reloader=False)  # Cambia app.run() por socketio.run()
