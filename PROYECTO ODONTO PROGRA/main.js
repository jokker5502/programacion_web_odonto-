

document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA PARA EL MODAL DE ÉXITO (POP-UP) ---
    const modal = document.getElementById('successModal');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.get('submission') === 'success') {
        if(modal) modal.classList.add('is-active');
    }

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', () => modal.classList.remove('is-active'));
    }

    if (modal) {
        modal.addEventListener('click', event => {
            if (event.target === modal) {
                modal.classList.remove('is-active');
            }
        });
    }
    const userAvatarBtn = document.getElementById('userAvatarBtn');
    const userMenu = document.getElementById('userMenu');

    if (userAvatarBtn) {
        userAvatarBtn.addEventListener('click', function(event) {
            event.stopPropagation(); // Evita que el clic se propague al documento
            userMenu.classList.toggle('is-active');
        });
    }
    // Cierra el menú si se hace clic en cualquier otro lugar
    document.addEventListener('click', function() {
        if (userMenu && userMenu.classList.contains('is-active')) {
            userMenu.classList.remove('is-active');
        }
    });
});