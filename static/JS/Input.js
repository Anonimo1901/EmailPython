document.addEventListener("DOMContentLoaded", function () {
    const fileInputExcel = document.getElementById('archivo');
    const fileNameExcel = document.getElementById('file-name');
    const fileInputEnviar = document.getElementById('imagen');
    const fileNameEnviar = document.getElementById('file-name-enviar');

    fileInputExcel.addEventListener('change', function () {
        const fileName = this.files[0]?.name || "Ningún archivo seleccionado";
        fileNameExcel.textContent = fileName;
        fileNameExcel.style.display = 'inline';
    });

    fileInputEnviar.addEventListener('change', function () {
        const fileName = this.files[0]?.name || "Ningún archivo seleccionado";
        fileNameEnviar.textContent = fileName;
        fileNameEnviar.style.display = 'inline';
    });
});
