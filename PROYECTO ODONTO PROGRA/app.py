from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date # Necesario para manejar fechas y horas
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- Configuración de la Base de Datos ---
# Asegúrate de reemplazar 'TU_USUARIO', 'TU_CONTRASEÑA' y 'localhost' si es diferente.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kjkm10000202++@localhost/neosmile'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_llave_secreta_muy_secreta'  # ¡Importante para mensajes flash!

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'ruta_acceso' # <-- A qué ruta redirigir si alguien intenta acceder a una página protegida sin iniciar sesión.
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "info" # Categoría para mensajes flash

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login usa esta función para recargar el objeto de usuario desde el ID de usuario almacenado en la sesión
    return Paciente.query.get(int(user_id))

# --- Modelos de la Base de Datos (Representación de tus tablas SQL en Python) ---
# Estos modelos deben coincidir con las tablas que creaste en tu base de datos "neosmile".

# En app.py, reemplaza tu clase Paciente con esta:
class Paciente(db.Model, UserMixin): # <-- Añadimos UserMixin
    __tablename__ = 'Pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # <-- NUEVA COLUMNA
    telefono = db.Column(db.String(20), nullable=True)
    edad = db.Column(db.Integer, nullable=True)
    fecha_registro = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    citas = db.relationship('Cita', backref='paciente_info', lazy=True)

    # Para que Flask-Login sepa cuál es el ID único
    def get_id(self):
       return (self.id_paciente)

    # Método para "hashear" la contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar la contraseña
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Especialidad(db.Model):
    __tablename__ = 'Especialidades'
    id_especialidad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_especialidad = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    # Relaciones
    citas = db.relationship('Cita', backref='especialidad_info', lazy=True)
    especialistas = db.relationship('Especialista', backref='especialidad_asignada_info', lazy=True)

class Especialista(db.Model):
    __tablename__ = 'Especialistas'
    id_especialista = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    id_especialidad = db.Column(db.Integer, db.ForeignKey('Especialidades.id_especialidad'))
    correo_electronico = db.Column(db.String(255), unique=True, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    # Relación
    citas = db.relationship('Cita', backref='especialista_info', lazy=True)

class Cita(db.Model):
    __tablename__ = 'Citas'
    id_cita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Pacientes.id_paciente'), nullable=True)
    nombre_completo_cita = db.Column(db.String(255), nullable=False)
    correo_cita = db.Column(db.String(255), nullable=False)
    telefono_cita = db.Column(db.String(20), nullable=False)
    edad_cita = db.Column(db.Integer, nullable=True)
    id_especialidad_requerida = db.Column(db.Integer, db.ForeignKey('Especialidades.id_especialidad'), nullable=False)
    id_especialista_preferido = db.Column(db.Integer, db.ForeignKey('Especialistas.id_especialista'), nullable=True)
    fecha_cita = db.Column(db.Date, nullable=False)
    hora_cita = db.Column(db.Time, nullable=False)
    motivo_consulta = db.Column(db.Text, nullable=True)
    fecha_solicitud = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    estado_cita = db.Column(db.Enum('Pendiente', 'Confirmada', 'Cancelada', 'Completada'), default='Pendiente')

class Emergencia(db.Model):
    __tablename__ = 'Emergencias'
    id_emergencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo_usuario = db.Column(db.String(255), nullable=False)
    telefono_contacto = db.Column(db.String(20), nullable=False)
    tipo_emergencia = db.Column(db.String(100), nullable=False)
    descripcion_emergencia = db.Column(db.Text, nullable=True)
    fecha_solicitud = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    estado_emergencia = db.Column(db.Enum('Recibida', 'En Proceso', 'Atendida'), default='Recibida')

class MensajeContacto(db.Model):
    __tablename__ = 'MensajesContacto'
    id_mensaje = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False) # Asegúrate que el nombre del campo coincida con el form
    servicio_interes = db.Column(db.String(100), nullable=True)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    estado_mensaje = db.Column(db.Enum('No leído', 'Leído', 'Respondido'), default='No leído')


# --- Rutas (Endpoints de tu aplicación) ---

# Ruta para la página de Inicio
@app.route('/')
def ruta_inicio():
    return render_template('Inicio.html') # Renderiza Inicio.html desde la carpeta templates/

@app.route('/acceso')
def ruta_acceso():
    # Esta función simplemente mostrará la página con los formularios de login y registro.
    # Asume que tienes un archivo llamado 'SingIn.html' o 'Acceso.html' en tu carpeta 'templates'.
    return render_template('SingIn.html')


@app.route('/login', methods=['POST'])
def ruta_login():
    correo = request.form.get('correo')
    password = request.form.get('password')
    
    # Buscar al paciente por correo
    paciente = Paciente.query.filter_by(correo_electronico=correo).first()
    
    # Verificar si el paciente existe y si la contraseña es correcta
    if not paciente or not paciente.check_password(password):
        flash('Correo electrónico o contraseña incorrectos. Por favor, intenta de nuevo.', 'danger')
        return redirect(url_for('ruta_acceso'))
    
    # Si todo es correcto, iniciamos la sesión del usuario
    login_user(paciente)
    flash(f'¡Bienvenido de nuevo, {paciente.nombre_completo}!', 'success')
    
    # Redirigir a la página de agendar cita o a un futuro "dashboard"
    return redirect(url_for('ruta_agendar_cita'))

# En app.py, reemplaza tu función ruta_registro con esta:

# En app.py

@app.route('/registro', methods=['POST'])
def ruta_registro():
    # Obtenemos todos los datos del formulario de registro
    nombre = request.form.get('nombre_completo')
    correo = request.form.get('correo')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    telefono = request.form.get('telefono')
    fecha_nacimiento_str = request.form.get('fecha_nacimiento')

    # --- VALIDACIONES SECUENCIALES ---

    # 1. ¿Correo electrónico ya existe?
    usuario_existente = Paciente.query.filter_by(correo_electronico=correo).first()
    if usuario_existente:
        flash('El correo electrónico ya está en uso. Por favor, elige otro o inicia sesión.', 'danger')
        return redirect(url_for('ruta_acceso'))

    # 2. ¿Las contraseñas no coinciden?
    if password != confirm_password:
        flash('Las contraseñas no coinciden. Por favor, vuelve a intentarlo.', 'danger')
        return redirect(url_for('ruta_acceso'))
        
    # 3. ¿El correo tiene un '@'?
    if '@' not in correo:
        flash('El formato del correo electrónico no es válido.', 'danger')
        return redirect(url_for('ruta_acceso'))

    # 4. ¿El teléfono tiene 10 dígitos (si se proporcionó)?
    if telefono and (not telefono.isdigit() or len(telefono) != 10):
        flash('El número de teléfono debe contener exactamente 10 dígitos numéricos.', 'danger')
        return redirect(url_for('ruta_acceso'))
        
    # 5. ¿La fecha de nacimiento es válida y el usuario es mayor de 18?
    if not fecha_nacimiento_str:
        flash('La fecha de nacimiento es un campo obligatorio.', 'danger')
        return redirect(url_for('ruta_acceso'))
        
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        if edad < 18:
            flash('Debes ser mayor de 18 años para poder registrarte.', 'danger')
            return redirect(url_for('ruta_acceso'))
    except ValueError:
        flash('El formato de la fecha de nacimiento no es válido.', 'danger')
        return redirect(url_for('ruta_acceso'))

    # --- SI TODO ESTÁ CORRECTO ---

    # Si pasamos todas las validaciones, creamos el nuevo paciente
    nuevo_paciente = Paciente(
        nombre_completo=nombre,
        correo_electronico=correo,
        telefono=telefono
        # Nota: No guardamos la edad, sino la fecha de nacimiento si tuvieras esa columna.
    )
    nuevo_paciente.set_password(password) # ¡Guardamos la contraseña encriptada!
    
    db.session.add(nuevo_paciente)
    db.session.commit()
    
    # ¡Mensaje de Éxito!
    flash('¡Felicidades! Te has registrado correctamente. Ahora puedes iniciar sesión.', 'success')
    return redirect(url_for('ruta_acceso'))

@app.route('/logout')
@login_required # Solo alguien logueado puede desloguearse
def ruta_logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('ruta_inicio'))

# En app.py
@app.route('/especialidades')
def ruta_especialidades():
    # Consultamos todos los especialistas desde la base de datos
    especialistas = Especialista.query.all()
    # Se los pasamos a la plantilla
    return render_template('NuestrasEspecialidades.html', especialistas_db=especialistas)

# Ruta para la página de Contacto (GET para mostrar, POST para procesar el formulario)
@app.route('/contacto', methods=['GET', 'POST'])
def ruta_contacto():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario de contacto.html
            # Asegúrate que los atributos 'name' en tu HTML coincidan con request.form['...']
            nombre = request.form['nombre_completo'] # Asumiendo que el input tiene name="nombre_completo"
            email = request.form['correo_electronico'] # Asumiendo name="correo_electronico"
            telefono_form = request.form['telefono'] # Asumiendo name="telefono"
            servicio = request.form['servicio_interes'] # Asumiendo name="servicio_interes"
            mensaje_form = request.form['mensaje'] # Asumiendo name="mensaje"

            nuevo_mensaje = MensajeContacto(
                nombre_completo=nombre,
                correo_electronico=email,
                telefono=telefono_form,
                servicio_interes=servicio,
                mensaje=mensaje_form
            )
            db.session.add(nuevo_mensaje)
            db.session.commit()
            flash('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success')
            return redirect(url_for('ruta_contacto')) # Redirige a la misma página de contacto (método GET)
        except Exception as e:
            db.session.rollback() # Deshacer cambios en caso de error
            flash(f'Error al enviar el mensaje: {str(e)}', 'danger')
            app.logger.error(f"Error al guardar mensaje de contacto: {e}")


    # Para el método GET (cuando el usuario solo visita la página)
    # Puedes pasar datos dinámicos a tu plantilla si es necesario
    # Ejemplo: servicios = Especialidad.query.all()
    # return render_template('contacto.html', servicios_para_dropdown=servicios)
    return render_template('contacto.html')


# Ruta para la página de Agendar Cita
@app.route('/agendar-cita', methods=['GET', 'POST'])
@login_required
def ruta_agendar_cita():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            telefono = request.form['telefono']
            edad_str = request.form.get('edad')
            edad = int(edad_str) if edad_str and edad_str.isdigit() else None

            id_especialidad = request.form['especialidad'] # Este será el ID de la especialidad
            id_especialista_str = request.form.get('especialista') # Puede estar vacío
            id_especialista = int(id_especialista_str) if id_especialista_str and id_especialista_str.isdigit() else None

            fecha_str = request.form['fecha']
            hora_str = request.form['hora']
            motivo = request.form.get('motivo')

            # Convertir string de fecha y hora a objetos de Python
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora_str, '%H:%M').time()

            nueva_cita = Cita(
                nombre_completo_cita=nombre,
                correo_cita=correo,
                telefono_cita=telefono,
                edad_cita=edad,
                id_especialidad_requerida=int(id_especialidad),
                id_especialista_preferido=id_especialista,
                fecha_cita=fecha_obj,
                hora_cita=hora_obj,
                motivo_consulta=motivo
            )
            db.session.add(nueva_cita)
            db.session.commit()
            flash('Cita agendada con éxito. Te contactaremos para confirmar.', 'success')
            return redirect(url_for('ruta_agendar_cita'))
        
        except ValueError as ve: # Errores de conversión de tipo (ej. string a int)
            db.session.rollback()
            flash(f'Error en los datos del formulario: {ve}. Por favor, revisa los campos.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al agendar la cita: {e}', 'danger')
            app.logger.error(f"Error al guardar cita: {e}")


    # Para el método GET: cargar especialidades y especialistas para los dropdowns
    especialidades_db = Especialidad.query.order_by(Especialidad.nombre_especialidad).all()
    especialistas_db = Especialista.query.order_by(Especialista.nombre_completo).all()

    especialistas_list = []
    for doc in especialistas_db:
        especialistas_list.append({
            'id_especialista': doc.id_especialista,
            'nombre_completo': doc.nombre_completo,
            'id_especialidad': doc.id_especialidad
        })

    return render_template(
        'AgendarCita.html',
        especialidades_db=especialidades_db, 
        especialistas_list_json=especialistas_list # Pasamos la nueva lista formateada
    )


# Ruta para la página de Atención de Emergencias
# En app.py

@app.route('/atencion-emergencias', methods=['GET', 'POST'])
def ruta_atencion_emergencias():
    if request.method == 'POST':
        try:
            # --- CORRECCIÓN DE SINTAXIS AQUÍ ---
            # Usamos .get('...') con paréntesis
            nombre_usuario = request.form.get('nombre_usuario')
            telefono_contacto = request.form.get('telefono_contacto')
            tipo_emergencia = request.form.get('opciones') # Definimos la variable correctamente
            descripcion = request.form.get('descripcion')

            # --- CORRECCIÓN DE LÓGICA AQUÍ ---
            # Verificamos la variable que sí definimos
            if not tipo_emergencia:
                flash('Por favor, selecciona un tipo de emergencia.', 'danger')
                return redirect(url_for('ruta_atencion_emergencias'))

            nueva_solicitud_emergencia = Emergencia(
                nombre_completo_usuario=nombre_usuario,
                telefono_contacto=telefono_contacto,
                tipo_emergencia=tipo_emergencia, # <-- Ahora esta variable existe
                descripcion_emergencia=descripcion
            )
            db.session.add(nueva_solicitud_emergencia)
            db.session.commit()
            
            # Esto se mantiene igual para mostrar el pop-up
            return redirect(url_for('ruta_atencion_emergencias', submission='success'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al enviar la solicitud: {e}', 'danger')
            app.logger.error(f"Error al guardar emergencia: {e}")
            return redirect(url_for('ruta_atencion_emergencias'))

    # El método GET se mantiene igual
    return render_template('AtencionEmergencias.html')


# --- Bloque para ejecutar la aplicación ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crea las tablas en la base de datos si no existen, basado en los modelos

        # Opcional: Sembrar datos iniciales (ej. especialidades) si la tabla está vacía
        if Especialidad.query.count() == 0:
            print("Sembrando especialidades iniciales...")
            especialidades_iniciales = [
                Especialidad(nombre_especialidad="Odontología General", descripcion="Cuidado preventivo y tratamientos básicos."),
                Especialidad(nombre_especialidad="Ortodoncia", descripcion="Corrección de la posición dental."),
                Especialidad(nombre_especialidad="Estética Dental", descripcion="Mejora de la apariencia de la sonrisa."),
                Especialidad(nombre_especialidad="Implantología", descripcion="Reemplazo de dientes perdidos.")
            ]
            db.session.bulk_save_objects(especialidades_iniciales)
            db.session.commit()
            print("Especialidades sembradas.")
        
        # Opcional: Sembrar datos iniciales para Especialistas
        if Especialista.query.count() == 0 and Especialidad.query.count() > 0:
            print("Sembrando especialistas iniciales...")
            # Asumimos que las especialidades ya existen y obtenemos sus IDs
            od_general = Especialidad.query.filter_by(nombre_especialidad="Odontología General").first()
            ortodoncia = Especialidad.query.filter_by(nombre_especialidad="Ortodoncia").first()

            if od_general and ortodoncia: # Verificar que se encontraron las especialidades
                especialistas_iniciales = [
                    Especialista(nombre_completo="Dr. Carlos Dental", id_especialidad=od_general.id_especialidad),
                    Especialista(nombre_completo="Dra. Ana Sonrisa", id_especialidad=ortodoncia.id_especialidad),
                ]
                db.session.bulk_save_objects(especialistas_iniciales)
                db.session.commit()
                print("Especialistas sembrados.")
            else:
                print("No se pudieron sembrar especialistas porque no se encontraron las especialidades base.")


    app.run(debug=True) # Inicia el servidor de desarrollo de Flask