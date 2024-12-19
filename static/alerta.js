@app.route('/')
def index():
    # Puedes definir un mensaje a mostrar
    mensaje = "¡Correos enviados correctamente!"  # O cualquier otro mensaje
    return render_template('index.html', mensaje=mensaje)
