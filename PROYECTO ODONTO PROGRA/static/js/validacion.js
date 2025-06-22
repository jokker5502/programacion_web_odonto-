// static/js/validacion.js

document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.querySelector('form[action="{{ url_for(\'ruta_registro\') }}"]'); // Sé más específico si hay varios forms

    if (form) {
        form.addEventListener('submit', function(event) {
            let errorMessages = []; // Colección de todos los errores

            // Validación de campos requeridos
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (field.value.trim() === '') {
                    errorMessages.push('El campo "' + (field.labels[0] ? field.labels[0].innerText : field.name) + '" es obligatorio.');
                }
            });

            // Validación de teléfono
            const telefonoField = form.querySelector('#register_telefono');
            if (telefonoField && telefonoField.value.trim() !== '' && !/^\d{10}$/.test(telefonoField.value)) {
                errorMessages.push('El teléfono debe tener 10 dígitos.');
            }

            // Validación de edad
            const fechaNacimientoField = form.querySelector('#register_fecha_nacimiento');
            if (fechaNacimientoField && fechaNacimientoField.value) {
                const fechaNacimiento = new Date(fechaNacimientoField.value);
                const hoy = new Date();
                const edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
                const m = hoy.getMonth() - fechaNacimiento.getMonth();

                if (m < 0 || (m === 0 && hoy.getDate() < fechaNacimiento.getDate())) {
                    edad--;
                }

                if (edad < 18) {
                    errorMessages.push('Debes ser mayor de 18 años.');
                }
            }
            
            // Validación de contraseñas
            const passwordField = form.querySelector('#register_password');
            const confirmPasswordField = form.querySelector('#register_confirm_password');
            if (passwordField && confirmPasswordField && passwordField.value !== confirmPasswordField.value) {
                errorMessages.push('Las contraseñas no coinciden.');
            }


            // Si hay errores, previene el envío y los muestra
            if (errorMessages.length > 0) {
                event.preventDefault(); // Detiene el envío del formulario
                alert("Por favor, corrige los siguientes errores:\n\n" + errorMessages.join('\n'));
            }
        });
    }
});