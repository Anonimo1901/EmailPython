// Leer archivo Excel y cargar las columnas en los select
document.getElementById('archivo').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
    const file = event.target.files[0];  // Obtener el archivo Excel
    const reader = new FileReader();  // Crear un lector de archivos

    reader.onload = function (e) {
        const data = e.target.result;  // Obtener los datos del archivo
        const workbook = XLSX.read(data, { type: 'binary' });  // Leer el archivo Excel
        const sheetName = workbook.SheetNames[0];  // Obtener el nombre de la primera hoja
        const sheet = workbook.Sheets[sheetName];  // Obtener la primera hoja

        // Convertir la hoja de cálculo en un JSON de filas
        const rows = XLSX.utils.sheet_to_json(sheet);

        // Llamar a la función que llena los select con las columnas del archivo
        populateColumnSelectors(rows);
    };

    reader.readAsBinaryString(file);  // Leer el archivo como cadena binaria
}

// Llenar los select con las columnas del archivo Excel
function populateColumnSelectors(rows) {
    const columnNames = Object.keys(rows[0]);  // Obtener los nombres de las columnas
    const selectNombre = document.getElementById('columna_nombre');  // Select para nombre
    const selectEmail = document.getElementById('columna_email');  // Select para correo

    // Limpiar las opciones previas en ambos select
    selectNombre.innerHTML = '';
    selectEmail.innerHTML = '';

    // Agregar las opciones al select de nombre y correo
    columnNames.forEach(column => {
        const optionNombre = document.createElement('option');
        optionNombre.value = column;  // Asignar el valor de la columna
        optionNombre.textContent = column;  // Mostrar el nombre de la columna
        selectNombre.appendChild(optionNombre);  // Agregar la opción al select de nombre

        const optionEmail = document.createElement('option');
        optionEmail.value = column;  // Asignar el valor de la columna
        optionEmail.textContent = column;  // Mostrar el nombre de la columna
        selectEmail.appendChild(optionEmail);  // Agregar la opción al select de correo
    });
}