document.addEventListener("DOMContentLoaded", function () {
    // Modales de eliminación y edición
    const buttonsEliminar = document.querySelectorAll('.btn-eliminar');
    const buttonsEditar = document.querySelectorAll('.btn-editar');

    // Modales
    const modalEliminar = document.getElementById('myModal');
    const modalEditar = document.getElementById('editModal');

    // Elementos para cerrar los modales
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

            // Mostrar modal de eliminación
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

            // Mostrar modal de edición
            modalEditar.style.display = 'block';
        });
    });

    // Cerrar el modal de eliminación
    spanEliminar.onclick = function () {
        modalEliminar.style.display = 'none';
    };

    // Cerrar el modal de edición
    spanEditar.onclick = function () {
        modalEditar.style.display = 'none';
    };

    // Cerrar modales si se hace click fuera de ellos
    window.onclick = function (event) {
        if (event.target === modalEliminar) {
            modalEliminar.style.display = 'none';
        }
        if (event.target === modalEditar) {
            modalEditar.style.display = 'none';
        }
    };
});
