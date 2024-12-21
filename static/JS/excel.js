document.getElementById('archivo').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        const data = e.target.result;
        const workbook = XLSX.read(data, { type: 'binary' });
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];


        const rows = XLSX.utils.sheet_to_json(sheet);

        populateColumnSelectors(rows);
    };

    reader.readAsBinaryString(file);
}


function populateColumnSelectors(rows) {
    const columnNames = Object.keys(rows[0]);
    const selectNombre = document.getElementById('columna_nombre');
    const selectEmail = document.getElementById('columna_email');


    selectNombre.innerHTML = '';
    selectEmail.innerHTML = '';


    columnNames.forEach(column => {
        const optionNombre = document.createElement('option');
        optionNombre.value = column;
        optionNombre.textContent = column;
        selectNombre.appendChild(optionNombre);

        const optionEmail = document.createElement('option');
        optionEmail.value = column;
        optionEmail.textContent = column;
        selectEmail.appendChild(optionEmail);
    });
}