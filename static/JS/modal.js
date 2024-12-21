document.addEventListener("DOMContentLoaded", function () {
    const buttonsEliminar = document.querySelectorAll('.btn-eliminar');
    const buttonsEditar = document.querySelectorAll('.btn-editar');
    const modalEliminar = document.getElementById('myModal');
    const modalEditar = document.getElementById('editModal');

    buttonsEliminar.forEach(button => {
        button.addEventListener('click', function () {
            const nombre = button.getAttribute('data-nombre');
            const correo = button.getAttribute('data-correo');
            document.getElementById('cliente-nombre').value = nombre;
            document.getElementById('correo-cliente').value = correo;
            document.getElementById('correo-cliente-hidden').value = correo;
            modalEliminar.style.display = 'block';
        });
    });

    buttonsEditar.forEach(button => {
        button.addEventListener('click', function () {
            const nombre = button.getAttribute('data-nombre');
            const correo = button.getAttribute('data-correo');
            document.getElementById('cliente-nombre-edit').value = nombre;
            document.getElementById('correo-cliente-edit').value = correo;
            document.getElementById('correo-cliente-hidden-edit').value = correo;
            modalEditar.style.display = 'block';
        });
    });

    const cancelarEliminar = document.getElementById('cancelar-eliminar');
    cancelarEliminar.addEventListener('click', function () {
        modalEliminar.style.display = 'none';
    });

    const cancelarEditar = document.getElementById('cancelar-editar');
    cancelarEditar.addEventListener('click', function () {
        modalEditar.style.display = 'none';
    });

    window.onclick = function (event) {
        if (event.target === modalEliminar) {
            modalEliminar.style.display = 'none';
        }
        if (event.target === modalEditar) {
            modalEditar.style.display = 'none';
        }
    };

    const fileInputImage = document.getElementById('imagen');
    const fileNameImage = document.getElementById('file-name-image');

    fileInputImage.addEventListener('change', function () {
        const fileName = this.files[0]?.name || "Ningún archivo seleccionado";
        fileNameImage.textContent = fileName;
        fileNameImage.style.display = 'inline';
    });
});
