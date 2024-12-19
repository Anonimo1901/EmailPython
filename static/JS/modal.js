document.addEventListener("DOMContentLoaded", function () {
    // Modales de eliminación y edición
    const buttonsEliminar = document.querySelectorAll('.btn-eliminar');
    const buttonsEditar = document.querySelectorAll('.btn-editar');

    // Modales
    const modalEliminar = document.getElementById('myModal');
    const modalEditar = document.getElementById('editModal');

    // Elementos para cerrar modales
    const spanEliminar = document.getElementsByClassName('close')[0];
    const spanEditar = document.getElementsByClassName('close')[1];

    // Formularios
    const formularioEliminar = document.getElementById('form-eliminar-cliente');
    const formularioEditar = document.getElementById('form-edit-client');

    // Función para mostrar el modal de eliminar cliente
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

    // Función para mostrar el modal de editar cliente
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

    // Cerrar los modales al hacer click en la "X" o fuera del modal
    spanEliminar.onclick = function () {
        modalEliminar.style.display = 'none';
    };
    spanEditar.onclick = function () {
        modalEditar.style.display = 'none';
    };

    window.onclick = function (event) {
        if (event.target === modalEliminar) {
            modalEliminar.style.display = 'none';
        }
        if (event.target === modalEditar) {
            modalEditar.style.display = 'none';
        }
    };
});
