document.addEventListener('DOMContentLoaded', function() {
    const locationSelect = document.getElementById('location-select');
    const mapDisplay = document.getElementById('map-display');

    locationSelect.addEventListener('change', function() {
        const location = this.value;
        updateMap(location);
    });

    function updateMap(location) {
        let mapData = {
            'sede-cumbaya': {
                url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3989.7980943280536!2d-78.43050562556754!3d-0.20746979981669232!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x91d5bd30d9536d5b%3A0x7f1f7f69a18ce195!2sCumbay%C3%A1%2C%20Quito%2C%20Ecuador!5e0!3m2!1sen!2sus!4v1716510647342!5m2!1sen!2sus',
                title: 'Sede Cumbaya',
                address: 'Av. Interoceánica, Cumbayá, Quito, Ecuador',
                link: 'https://maps.app.goo.gl/eGJbDzhGhK1ahYiU6'
            },
            'sede-norte': {
                url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3989.75998709308!2d-78.49300802556749!3d-0.18310509981401523!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x91d59a4002427c9f%3A0x44b991e158ef5572!2sQuito%2C%20Ecuador!5e0!3m2!1sen!2sus!4v1716510744990!5m2!1sen!2sus',
                title: 'Sede Norte',
                address: 'Av. Amazonas y Naciones Unidas, Quito, Ecuador',
                link: 'https://maps.app.goo.gl/UzSYb7sNx99MvUp49'
            }
        };

        // Limpiar el contenido del mapa
        mapDisplay.innerHTML = '';

        // Verificar si la ubicación existe en los datos
        if (mapData[location]) {
            const data = mapData[location];
            mapDisplay.innerHTML = `
                <div class="location-info">
                    <h3 class="location-title">${data.title}</h3>
                    <p class="location-address">${data.address}</p>
                </div>
                <iframe 
                    src="${data.url}" 
                    class="map-iframe" 
                    allowfullscreen="false" 
                    loading="lazy" 
                    referrerpolicy="no-referrer-when-downgrade" 
                    title="Mapa de ${data.title}">
                </iframe>
                <div style="padding: 16px;">
                    <a href="${data.link}" target="_blank" rel="noopener noreferrer" class="map-link">
                        <button class="map-button">Ver en Google Maps</button>
                    </a>
                </div>
            `;
        }
    }
});
