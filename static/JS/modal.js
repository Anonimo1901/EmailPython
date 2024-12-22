document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById('seleccionar-todo');
    const clienteCheckboxes = document.querySelectorAll('.checkbox-cliente');
    const btnEditarSeleccionado = document.getElementById('btn-editar-seleccionado');
    const btnEliminarSeleccionados = document.getElementById('btn-eliminar-seleccionados');
    const editModal = document.getElementById('editModal');
    const deleteModalSingle = document.getElementById('deleteModalSingle');
    const deleteModalMultiple = document.getElementById('deleteModalMultiple');
    const formEditClient = document.getElementById('form-edit-client');
    const formEliminarClientes = document.getElementById('form-eliminar-clientes');

    function updateButtonStates() {
        const checkedCheckboxes = document.querySelectorAll('.checkbox-cliente:checked');
        btnEditarSeleccionado.disabled = checkedCheckboxes.length !== 1;
        btnEliminarSeleccionados.disabled = checkedCheckboxes.length === 0;
    }

    selectAllCheckbox.addEventListener('change', function() {
        clienteCheckboxes.forEach(checkbox => checkbox.checked = this.checked);
        updateButtonStates();
    });

    clienteCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateButtonStates);
    });

    btnEditarSeleccionado.addEventListener('click', function() {
        const selectedCheckbox = document.querySelector('.checkbox-cliente:checked');
        if (selectedCheckbox) {
            const clienteInfo = selectedCheckbox.closest('li').querySelector('.cliente-info').textContent;
            const [nombre, correo] = clienteInfo.split(': ');
            document.getElementById('cliente-nombre-edit').value = nombre;
            document.getElementById('correo-cliente-edit').value = correo;
            document.getElementById('correo-cliente-hidden-edit').value = correo;
            editModal.style.display = 'block';
        }
    });

    btnEliminarSeleccionados.addEventListener('click', function() {
        const checkedCheckboxes = document.querySelectorAll('.checkbox-cliente:checked');
        const clientesAEliminar = document.getElementById('clientes-a-eliminar');
        clientesAEliminar.innerHTML = '';

        checkedCheckboxes.forEach(checkbox => {
            const clienteInfo = checkbox.closest('li').querySelector('.cliente-info').textContent;
            const clienteElement = document.createElement('div');
            clienteElement.textContent = clienteInfo;
            clienteElement.innerHTML += `<input type="hidden" name="correos_eliminar" value="${checkbox.value}">`;
            clientesAEliminar.appendChild(clienteElement);
        });

        deleteModalMultiple.style.display = 'block';
    });

    function closeModal(modal) {
        modal.style.display = 'none';
    }

    document.getElementById('cancelar-editar').addEventListener('click', function() {
        closeModal(editModal);
    });

    document.getElementById('cancelar-eliminar-single').addEventListener('click', function() {
        closeModal(deleteModalSingle);
    });

    document.getElementById('cancelar-eliminar-multiple').addEventListener('click', function() {
        closeModal(deleteModalMultiple);
    });

    window.onclick = function(event) {
        if (event.target === editModal) {
            closeModal(editModal);
        }
        if (event.target === deleteModalSingle) {
            closeModal(deleteModalSingle);
        }
        if (event.target === deleteModalMultiple) {
            closeModal(deleteModalMultiple);
        }
    };

    formEditClient.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Cliente editado correctamente');
                window.location.reload();
            } else {
                alert('Error al editar el cliente: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al editar el cliente');
        });
    });

    formEliminarClientes.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Cliente(s) eliminado(s) correctamente');
                window.location.reload();
            } else {
                alert('Error al eliminar cliente(s): ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar cliente(s)');
        });
    });
});

