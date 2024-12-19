document.addEventListener('DOMContentLoaded', function() {
    const seleccionarTodo = document.getElementById('seleccionar-todo');
    const checkboxesClientes = document.querySelectorAll('.checkbox-cliente');

    seleccionarTodo.addEventListener('change', function() {
        checkboxesClientes.forEach(function(checkbox) {
            checkbox.checked = seleccionarTodo.checked;
        });
    });
});
