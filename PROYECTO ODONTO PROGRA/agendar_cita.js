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

    const autofillBtn = document.getElementById('autofillBtn');
    if (autofillBtn) {
        // 'userData' es la variable que pasaremos desde Flask
        if (typeof userData !== 'undefined') {
            autofillBtn.addEventListener('click', function() {
                document.getElementById('nombre').value = userData.nombre_completo || '';
                document.getElementById('correo').value = userData.correo_electronico || '';
                document.getElementById('telefono').value = userData.telefono || '';
                // No podemos autollenar la fecha de nacimiento porque el modelo Paciente no la tiene.
            });
        } else {
            autofillBtn.style.display = 'none'; // Oculta el botón si no hay datos de usuario
        }
    }

    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        const hoy = new Date();
        const anio = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, '0'); // +1 porque los meses son 0-11
        const dia = String(hoy.getDate()).padStart(2, '0');
        
        const fechaDeHoy = `${anio}-${mes}-${dia}`;
        fechaInput.setAttribute('min', fechaDeHoy);
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
        // En agendar_cita.js
    const fechaInput = document.getElementById('fecha');
    const especialistaSelect = document.getElementById('especialista');

    async function cargarHorarios() {
        const doctorId = especialistaSelect.value;
        const fecha = fechaInput.value;
        const slotsContainer = document.getElementById('time-slots-container');
        const horaInputOculto = document.getElementById('hora');

        if (!doctorId || !fecha) return;

        slotsContainer.innerHTML = '<p>Cargando horarios...</p>';
        horaInputOculto.value = '';

        const response = await fetch(`/api/horarios-disponibles/${doctorId}/${fecha}`);
        const horarios = await response.json();

        slotsContainer.innerHTML = '';
        if (horarios.length > 0) {
            horarios.forEach(hora => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'btn time-slot-btn';
                btn.textContent = hora;
                btn.onclick = () => {
                    // Des-seleccionar otros botones
                    document.querySelectorAll('.time-slot-btn.selected').forEach(b => b.classList.remove('selected'));
                    // Seleccionar este
                    btn.classList.add('selected');
                    horaInputOculto.value = hora;
                };
                slotsContainer.appendChild(btn);
            });
        } else {
            slotsContainer.innerHTML = '<p>No hay horarios disponibles para este día.</p>';
        }
    }
    fechaInput.addEventListener('change', cargarHorarios);
    especialistaSelect.addEventListener('change', cargarHorarios);
});

