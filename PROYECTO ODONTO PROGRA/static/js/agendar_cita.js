// Este código se ejecuta cuando todo el contenido del HTML ha sido cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // Obtener referencias a los dos menús desplegables
    const especialidadSelect = document.getElementById('especialidad');
    const especialistaSelect = document.getElementById('especialista');

    // 'todosLosEspecialistas' es una variable global que definiremos en AgendarCita.html
    // y que contendrá la lista completa de doctores que viene desde Flask.
    if (typeof todosLosEspecialistas === 'undefined') {
        console.error("La lista de especialistas (todosLosEspecialistas) no está definida.");
        return;
    }

    // Añadir un "escuchador de eventos" que se activa cuando cambia la selección de especialidad
    especialidadSelect.addEventListener('change', function() {
        
        // 1. Obtener el ID de la especialidad seleccionada
        const selectedEspecialidadId = this.value;

        // 2. Limpiar las opciones actuales del dropdown de especialistas
        especialistaSelect.innerHTML = '';

        // 3. Añadir la opción por defecto ("Seleccione un especialista...")
        let defaultOption = document.createElement('option');
        defaultOption.value = "";
        defaultOption.textContent = 'Seleccione un especialista si lo desea';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        especialistaSelect.appendChild(defaultOption);

        // 4. Filtrar la lista completa de especialistas
        // Busca solo los doctores cuyo id_especialidad coincida con el seleccionado
        const especialistasFiltrados = todosLosEspecialistas.filter(function(especialista) {
            return especialista.id_especialidad == selectedEspecialidadId;
        });

        // 5. Poblar el dropdown de especialistas con los resultados filtrados
        if (especialistasFiltrados.length > 0) {
            especialistasFiltrados.forEach(function(especialista) {
                let option = document.createElement('option');
                option.value = especialista.id_especialista;
                option.textContent = especialista.nombre_completo;
                especialistaSelect.appendChild(option);
            });
        }
    });
});