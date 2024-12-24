document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formulario-correos");
    const loadingModal = document.getElementById('loadingModal');

    // Función para mostrar el modal
    function mostrarModal() {
        loadingModal.style.display = 'flex';
    }

    // Función para ocultar el modal
    function ocultarModal() {
        loadingModal.style.display = 'none';
    }

    formulario.addEventListener("submit", function (event) {
        event.preventDefault(); // Detener el envío inmediato

        const checkboxes = document.querySelectorAll('.checkbox-cliente:checked');

        if (checkboxes.length > 0) {
            // Enviar el formulario primero
            formulario.submit();

            // Mostrar el modal de carga después de enviar el formulario
            mostrarModal();

            // Simulando un proceso de envío con setTimeout para mantener el modal visible
            // Este setTimeout es solo un simulador, no es necesario si ya se ha enviado el formulario
        } else {
            alert('Hubo un error, selecciona al menos un cliente');
        }
    });
});
