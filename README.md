Descripción:
Este sistema está diseñado para ofrecer una plataforma eficiente y fácil de usar para el envío masivo de correos electrónicos. Permite a los usuarios agregar contactos de manera manual o mediante la importación de archivos Excel. Además, incluye opciones para gestionar y actualizar la base de datos de clientes de manera sencilla. La plataforma facilita la adición, edición y eliminación de contactos, optimizando el proceso de gestión de contactos. Además, permite enviar mensajes personalizados, tanto en formato de texto como con imágenes adjuntas, mejorando la comunicación efectiva con los destinatarios.

¿Cómo lo hice?
La implementación del sistema se llevó a cabo con una página principal que sirve como interfaz de usuario. El diseño incluye funcionalidades como:

Selección de contactos: Los usuarios pueden seleccionar manualmente o de manera total los clientes ingresados mediante checkboxes.
Gestión de contactos: Botones para editar y eliminar contactos de forma sencilla.
Composición de mensajes: Un área de texto para escribir el asunto y cuerpo del mensaje, con la opción de adjuntar imágenes. Además, incluye un botón para enviar el correo.
Importación de contactos desde Excel: Los usuarios pueden cargar nombres y correos electrónicos desde un archivo Excel, especificando las columnas a importar.
Herramientas y Tecnologías Utilizadas:
Para desarrollar este sistema se emplearon varias tecnologías y herramientas que facilitaron tanto el desarrollo como la funcionalidad:

Flask: Framework principal para el desarrollo de la aplicación web.

Librerías utilizadas:

os, json, Flask, Flask-Mail, render_template, session, request, blueprint, redirect, url_for, current_app (para gestión de sesiones y rutas).
Pandas (para manipulación de datos, especialmente para la carga y gestión de los contactos desde Excel).
Lucide (para iconos en la interfaz de usuario).
XLSX.js: Para la importación de archivos Excel a través de JavaScript (CDN: XLSX.js).
Lenguajes utilizados:

Python: Para la lógica del backend y la manipulación de datos.
HTML, CSS, JavaScript: Para la creación de la interfaz de usuario interactiva.
JSON: Para almacenar y gestionar los datos de clientes y remitentes de forma estructurada.
Instalaciones adicionales con pip:


- flask: Framework
- flask-mail: Extensión de Flask para enviar correos electrónicos
- pandas: Necesario para el manejo de archivos Excel
- openpyxl: Requerido por pandas para leer archivos Excel

Objetivo:
El objetivo principal de este sistema es facilitar las tareas de marketing digital al proporcionar una herramienta sencilla para la gestión y el envío masivo de correos electrónicos. A largo plazo, se planea integrar una funcionalidad adicional que permita identificar empresas con intereses comunes, con el fin de establecer relaciones comerciales y aumentar las probabilidades de conversión de estas empresas en clientes potenciales.

