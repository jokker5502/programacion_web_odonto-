// static/js/contacto.js

document.addEventListener('DOMContentLoaded', function() {
    
    const whatsappButton = document.getElementById('btn_whatsapp');

    if (whatsappButton) {
        whatsappButton.addEventListener('click', function() {
            // 1. Obtiene el servicio seleccionado
            var servicioSelect = document.getElementById('whatsapp_servicio');
            var servicio = servicioSelect.options[servicioSelect.selectedIndex].text;

            // 2. Define tu número de teléfono (reemplaza con tu número real)
            var telefono = '593991234567'; // ¡REEMPLAZAR CON TU NÚMERO!

            // 3. Crea el mensaje pre-llenado
            var mensaje = 'Hola, quisiera más información sobre el servicio de ' + servicio + '.';

            // 4. Codifica el mensaje para la URL
            var mensajeCodificado = encodeURIComponent(mensaje);

            // 5. Construye la URL final
            var urlWhatsApp = 'https://wa.me/' + telefono + '?text=' + mensajeCodificado;

            // 6. Abre WhatsApp en una nueva pestaña
            window.open(urlWhatsApp, '_blank');
        });
    }
});