from flask import Blueprint, request, session, redirect, url_for
import pandas as pd
from routes.clientes import cargar_clientes, guardar_clientes

# Crear Blueprint para las rutas de Excel
excel_bp = Blueprint('excel', __name__)

# Función para agregar clientes desde un archivo Excel
def agregar_clientes_desde_excel(archivo, columna_nombre, columna_email):
    # Leer el archivo Excel
    df = pd.read_excel(archivo)

    # Cargar los clientes actuales
    clientes = cargar_clientes()

    # Agregar cada cliente del Excel al listado de clientes
    for _, row in df.iterrows():
        cliente = {
            "nombre": row[columna_nombre],
            "correo": row[columna_email]
        }
        clientes.append(cliente)

    # Guardar la lista de clientes actualizada
    guardar_clientes(clientes)

# Ruta para cargar clientes desde un archivo Excel
@excel_bp.route('/agregar_clientes_excel', methods=['POST'])
def agregar_clientes_excel():
    archivo = request.files['archivo']
    columna_nombre = request.form['columna_nombre']
    columna_email = request.form['columna_email']

    # Usamos la función para agregar los clientes desde Excel
    agregar_clientes_desde_excel(archivo, columna_nombre, columna_email)

    session['mensaje'] = 'Clientes agregados correctamente desde Excel.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))
