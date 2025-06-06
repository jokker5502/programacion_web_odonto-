// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    
    const navToggle = document.querySelector('.nav-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            // Alterna la clase 'is-active' para mostrar/ocultar el menú
            mainNav.classList.toggle('is-active');
        });
    }

});

// En static/js/main.js, dentro del evento DOMContentLoaded

document.addEventListener('DOMContentLoaded', function() {
    
    // ... (tu código del menú de hamburguesa va aquí arriba) ...

    // --- LÓGICA PARA EL MODAL DE ÉXITO ---
    const modal = document.getElementById('successModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    
    // 1. Revisa si la URL tiene el parámetro ?submission=success
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('submission') === 'success') {
        if(modal) modal.classList.add('is-active');
    }

    // 2. Cierra el modal al hacer clic en el botón "Entendido"
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', function() {
            modal.classList.remove('is-active');
        });
    }

    // 3. Cierra el modal al hacer clic fuera de él (en el fondo oscuro)
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.classList.remove('is-active');
            }
        });
    }
});