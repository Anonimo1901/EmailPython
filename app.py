from flask import Flask, render_template, session
from config import Config
from flask_mail import Mail
from routes.clientes import clientes_bp
from routes.correo import correo_bp
from routes.excel_utils import excel_bp

app = Flask(__name__)


Config.init_app(app)


app.mail = Mail(app)


app.register_blueprint(correo_bp, url_prefix='/correo')
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(excel_bp, url_prefix='/excel')


@app.route('/')
def index():

    from routes.clientes import cargar_clientes
    clientes = cargar_clientes()

    mensaje = None
    tipo_mensaje = None


    if 'mensaje' in session:
        mensaje = session['mensaje']
        tipo_mensaje = session['tipo_mensaje']
        session.pop('mensaje', None)
        session.pop('tipo_mensaje', None)

    return render_template('index.html', clientes=clientes, mensaje=mensaje, tipo_mensaje=tipo_mensaje)
@app.route('/p')
def base():
    return render_template('base.html')
if __name__ == '__main__':
    app.run(debug=True)
