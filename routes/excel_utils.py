from flask import Blueprint, request, session, redirect, url_for
import pandas as pd
from routes.clientes import cargar_clientes, guardar_clientes

excel_bp = Blueprint('excel', __name__)


def agregar_clientes_desde_excel(archivo, columna_nombre, columna_email):

    df = pd.read_excel(archivo)


    clientes = cargar_clientes()


    for _, row in df.iterrows():
        cliente = {
            "nombre": row[columna_nombre],
            "correo": row[columna_email]
        }
        clientes.append(cliente)


    guardar_clientes(clientes)


@excel_bp.route('/agregar_clientes_excel', methods=['POST'])
def agregar_clientes_excel():
    archivo = request.files['archivo']
    columna_nombre = request.form['columna_nombre']
    columna_email = request.form['columna_email']

    agregar_clientes_desde_excel(archivo, columna_nombre, columna_email)

    session['mensaje'] = 'Clientes agregados correctamente desde Excel.'
    session['tipo_mensaje'] = 'success'

    return redirect(url_for('index'))
