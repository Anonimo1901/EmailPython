import os
import json

class Config:
    # Cargar configuración del archivo config.json
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    MAIL_SERVER = 'smtp.gmail.com'  # Servidor SMTP de Gmail
    MAIL_PORT = 587  # Puerto para TLS
    MAIL_USE_TLS = True  # Usar TLS
    MAIL_USERNAME = config_data['remitente']  # Usar el remitente del archivo config.json
    MAIL_PASSWORD = config_data['contrasena']  # Usar la contraseña del archivo config.json
    
    SECRET_KEY = os.urandom(24)  # Clave secreta aleatoria

    @staticmethod
    def init_app(app):
        # Configurar la aplicación Flask con esta clase
        app.config.from_object(Config)
