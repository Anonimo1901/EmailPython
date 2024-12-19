
document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formulario-correos");
    const mensajeConfirmacion = document.getElementById("mensaje-confirmacion");
    const mensajeError = document.getElementById("mensaje-error");

    formulario.addEventListener("submit", function (event) {
        event.preventDefault();

        const checkboxes = document.querySelectorAll('.checkbox-cliente:checked');
        
        if (checkboxes.length > 0) {
            alert('Se envio correctanente')
            
            formulario.submit();
        } else {
            alert('Hubo un error')
        }
    });
});
