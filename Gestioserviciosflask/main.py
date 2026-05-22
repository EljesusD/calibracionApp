#Controlador del sistema de gestión de servicios de calibración

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from dao import DetalleOrden, LecturaTemperatura, Usuario, db, Equipo, Cliente, OrdenServicio, Empleado, Rol, ServicioCalibracion, ServicioEquipo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)


CORS(app, supports_credentials=True)#habilita rutas para la aplicacion movil
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:D3NaJ31992.@127.0.0.1/laboratorio_calibracion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "081021"  

db.init_app(app) #iniciamos

@app.route('/')
def index():
    if 'usuario_id' not in session:   # Verifica si hay sesión activa
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    return render_template('home.html')

'''--------------------------------------------------------------
Rutas para Autenticación
--------------------------------------------------------------'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.query.filter_by(username=username, activo=True).first()
        if usuario and usuario.check_password(password): 
            session['usuario_id'] = usuario.id_usuario
            session['usuario_username'] = usuario.username
            session['usuario_rol'] = usuario.empleado.rol.nombre.strip().lower()   

            flash(f'Bienvenido {usuario.username}. Tu rol es: {usuario.empleado.rol.nombre}', 'info')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

def roles_requeridos(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Debes iniciar sesión primero', 'warning')
                return redirect(url_for('login'))
            
            rol_actual = session.get('usuario_rol', '').strip().lower()
            roles_permitidos = [r.strip().lower() for r in roles]

            print("ROL EN SESIÓN:", rol_actual)  # Depuración
            print("ROLES PERMITIDOS:", roles_permitidos)

            if rol_actual not in roles_permitidos:
                flash(f'Acceso denegado. Tu rol es: {rol_actual}', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@roles_requeridos('administrador')  # Solo el rol de Administrador puede acceder a esta ruta
def crear_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        id_empleado = request.form['id_empleado']

        # Generar hash seguro de la contraseña
        password_hash = generate_password_hash(password)

        nuevo_usuario = Usuario(
            username=username,
            password_hash=password_hash,
            id_empleado=id_empleado,
            activo=True
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('listar_usuarios'))  # Ajusta según tu flujo

    return render_template('usuario/nuevo.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/panel')
def panel():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    return render_template('panel.html')

@app.route('/usuarios')
@roles_requeridos('administrador')  # Solo el rol de Administrador puede acceder a esta ruta
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuario/lista.html', usuarios=usuarios)




'''--------------------------------------------------------------
Rutas para Equipos
--------------------------------------------------------------'''
@app.route('/equipos')
@roles_requeridos('administrador', 'supervisor', 'técnico') 
def listar_equipos():
    cliente_id = request.args.get('cliente_id', type=int)
    if cliente_id:
        equipos = Equipo.query.filter_by(id_cliente=cliente_id).all()
    else:
        equipos = Equipo.query.all()

    clientes = Cliente.query.all()
    return render_template('equipo/lista_equipos.html', equipos=equipos, clientes=clientes, cliente_id=cliente_id)


@app.route('/agregar_equipo')
@roles_requeridos('administrador', 'supervisor', 'técnico')
def agregar_equipo():

    # Obtener lista de clientes y poder mostrarlos en el formulario de agregar equipo
    clientes = Cliente.query.order_by(Cliente.nombre_empresa).all()

    return render_template(
        'equipo/agregar_equipos.html',
        clientes=clientes
    )

@app.route('/nuevo_equipo', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')
def nuevo_equipo():

    nuevo = Equipo(
        nombre=request.form['nombre'],
        marca=request.form['marca'],
        modelo=request.form['modelo'],
        numero_serie=request.form['numero_serie'],
        rango_medicion=request.form['rango_medicion'],
        resolucion=request.form['resolucion'],
        id_cliente=request.form['id_cliente']
    )

    nuevo.agregar()

    return redirect(url_for('listar_equipos'))

@app.route('/importar_equipos_csv', methods=['POST'])
@roles_requeridos('administrador')
def importar_equipos_csv():
    if 'archivo_csv' not in request.files:
        flash('No se seleccionó archivo', 'danger')
        return redirect(url_for('listar_equipos'))

    archivo = request.files['archivo_csv']

    if archivo.filename == '':
        flash('Archivo vacío', 'danger')
        return redirect(url_for('listar_equipos'))

    try:
        df = pd.read_csv(archivo)

        for _, fila in df.iterrows():
            nuevo_equipo = Equipo(
                nombre=fila['nombre'],
                marca=fila['marca'],
                modelo=fila['modelo'],
                numero_serie=fila['numero_serie'],
                id_cliente=fila['id_cliente']
            )
            db.session.add(nuevo_equipo)

        db.session.commit()

        flash('Equipos importados correctamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar: {str(e)}', 'danger')

    return redirect(url_for('listar_equipos'))

@app.route('/editar_equipo/<int:id_equipo>', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def editar_equipo(id_equipo):
    # Obtener lista de clientes y poder mostrarlos en el formulario de editar equipo
    clientes = Cliente.query.order_by(Cliente.nombre_empresa).all()

    equipo = Equipo().consultaIndividual(id_equipo)
    if request.method == 'POST':
        equipo.nombre = request.form['nombre']
        equipo.marca = request.form['marca']
        equipo.modelo = request.form['modelo']
        equipo.numero_serie = request.form['numero_serie']
        equipo.rango_medicion = request.form['rango_medicion']
        equipo.resolucion = request.form['resolucion']
        equipo.id_cliente = request.form['id_cliente']
        equipo.editar()

        return redirect(url_for('listar_equipos'))
    #se pasan los clientes al template de editar equipo para mostrar en el formulario y poder seleccionar el cliente al que pertenece el equipo
    return render_template('equipo/editar_equipos.html', equipo=equipo, clientes=clientes)

@app.route('/eliminar_equipo/<int:id_equipo>', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def eliminar_equipo(id_equipo):
    Equipo().eliminar(id_equipo)
    return redirect(url_for('listar_equipos'))

'''--------------------------------------------------------------
Rutas para Clientes 
--------------------------------------------------------------'''

@app.route('/clientes')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder 
def listar_clientes():
    clientes = Cliente().consultaGeneral()
    return render_template('cliente/lista_clientes.html', clientes=clientes)

@app.route('/agregar_cliente')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def agregar_cliente():
    return render_template('cliente/agregar_cliente.html')

@app.route('/nuevo_cliente', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def nuevo_cliente():
    nuevo = Cliente(
        nombre_empresa=request.form['nombre_empresa'],
        contacto=request.form['contacto'],
        telefono=request.form['telefono'],
        correo=request.form['correo'],
        direccion=request.form['direccion']
    )
    nuevo.agregar()
    return redirect(url_for('listar_clientes'))

@app.route('/editar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder 
def editar_cliente(id_cliente):
    cliente = Cliente().consultaIndividual(id_cliente)
    if request.method == 'POST':
        cliente.nombre_empresa = request.form['nombre_empresa']
        cliente.contacto = request.form['contacto']
        cliente.telefono = request.form['telefono']
        cliente.correo = request.form['correo']
        cliente.direccion = request.form['direccion']
        cliente.editar()
        return redirect(url_for('listar_clientes'))
    return render_template('cliente/editar_cliente.html', cliente=cliente)

@app.route('/eliminar_cliente/<int:id_cliente>', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def eliminar_cliente(id_cliente):
    Cliente().eliminar(id_cliente)
    return redirect(url_for('listar_clientes'))

@app.route('/equipos_cliente/<int:id_cliente>')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def equipos_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return "Cliente no encontrado", 404
    return render_template('cliente/equipos_cliente.html', cliente=cliente)


'''--------------------------------------------------------------
Rutas para Ordenes de Servicio
--------------------------------------------------------------'''
@app.route('/ordenes')
@roles_requeridos('administrador', 'supervisor')
def listar_ordenes():
    ordenes = OrdenServicio().consultaGeneral()
    return render_template('orden/lista_ordenes.html', ordenes=ordenes)

@app.route('/agregar_orden')
@roles_requeridos('administrador', 'supervisor')
def agregar_orden():
    clientes = Cliente.query.all()
    empleados = Empleado.query.all()
    equipos = Equipo.query.all()
    servicios = ServicioCalibracion.query.all()
    return render_template(
        'orden/agregar_orden.html',
        clientes=clientes,
        empleados=empleados,
        equipos=equipos,
        servicios=servicios
    )
@app.route('/nueva_orden', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def nueva_orden():
    nueva = OrdenServicio(
        fecha_solicitud=request.form['fecha_solicitud'],
        estado=request.form['estado'],
        id_cliente=request.form['id_cliente'],
        id_empleado=request.form['id_empleado']
    )
    nueva.agregar()

# Crear detalle asociado
    detalle = DetalleOrden(
        id_orden=nueva.id_orden,
        id_equipo=request.form['id_equipo'],
        id_servicio=request.form['id_servicio'],
        fecha_inicio=request.form.get('fecha_inicio'),
        fecha_fin=request.form.get('fecha_fin'),
        resultado=request.form.get('resultado')
    )
    detalle.agregar()

    flash('Orden y detalle creados correctamente', 'success')
    return redirect(url_for('listar_detalles', id_orden=nueva.id_orden))


@app.route('/editar_orden/<int:id_orden>', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def editar_orden(id_orden):
    orden = OrdenServicio().consultaIndividual(id_orden)
    clientes = Cliente.query.all()
    empleados = Empleado.query.all()

    if request.method == 'POST':
        orden.fecha_solicitud = request.form['fecha_solicitud']
        orden.estado = request.form['estado']
        orden.id_cliente = request.form['id_cliente']
        orden.id_empleado = request.form['id_empleado']
        orden.editar()
        return redirect(url_for('listar_ordenes'))
    return render_template('orden/editar_orden.html', orden=orden, clientes=clientes, empleados=empleados)

@app.route('/eliminar_orden/<int:id_orden>', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def eliminar_orden(id_orden):
    OrdenServicio().eliminar(id_orden)
    return redirect(url_for('listar_ordenes'))


'''--------------------------------------------------------------
Rutas para Empleados
--------------------------------------------------------------'''


@app.route('/empleados')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def listar_empleados():
    empleados = Empleado().consultaGeneral()
    return render_template('empleado/lista_empleados.html', empleados=empleados)

@app.route('/agregar_empleado')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def agregar_empleado():
    roles = Rol.query.order_by(Rol.nombre).all() # se agrega para mostrar los roles disponibles en el formulario de agregar empleado
    return render_template('empleado/agregar_empleado.html', roles=roles) #roles=roles se agrega para pasar los roles al template de agregar empleado

@app.route('/nuevo_empleado', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def nuevo_empleado():
    nuevo = Empleado(
        nombre=request.form['nombre'],
        apellidos=request.form['apellidos'],
        correo=request.form['correo'],
        telefono=request.form['telefono'],
        direccion=request.form['direccion'],
        escolaridad=request.form['escolaridad'],
        id_rol=request.form['id_rol']
    )
    nuevo.agregar()
    return redirect(url_for('listar_empleados'))

@app.route('/editar_empleado/<int:id_empleado>', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def editar_empleado(id_empleado):
    empleado = Empleado().consultaIndividual(id_empleado)
    roles = Rol.query.order_by(Rol.nombre).all()
    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.apellidos = request.form['apellidos']
        empleado.correo = request.form['correo']
        empleado.telefono = request.form['telefono']
        empleado.direccion = request.form['direccion']
        empleado.escolaridad = request.form['escolaridad']
        empleado.id_rol = request.form['id_rol']
        empleado.editar()
        return redirect(url_for('listar_empleados'))
    return render_template('empleado/editar_empleado.html', empleado=empleado, roles=roles)

@app.route('/eliminar_empleado/<int:id_empleado>', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def eliminar_empleado(id_empleado):
    Empleado().eliminar(id_empleado)
    return redirect(url_for('listar_empleados'))
'''--------------------------------------------------------------
Rutas para Roles 
--------------------------------------------------------------'''
@app.route('/roles')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def listar_roles():
    roles = Rol().consultaGeneral()
    return render_template('rol/lista_roles.html', roles=roles)

@app.route('/agregar_rol')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def agregar_rol():
    return render_template('rol/agregar_rol.html')

@app.route('/nuevo_rol', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def nuevo_rol():
    nuevo = Rol(
        nombre=request.form['nombre'],
        descripcion=request.form['descripcion']
    )
    nuevo.agregar()
    return redirect(url_for('listar_roles'))

@app.route('/editar_rol/<int:id_rol>', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def editar_rol(id_rol):
    rol = Rol().consultaIndividual(id_rol)
    if request.method == 'POST':
        rol.nombre = request.form['nombre']
        rol.descripcion = request.form['descripcion']
        rol.editar()
        return redirect(url_for('listar_roles'))
    return render_template('rol/editar_rol.html', rol=rol)

@app.route('/eliminar_rol/<int:id_rol>', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def eliminar_rol(id_rol):
    Rol().eliminar(id_rol)
    return redirect(url_for('listar_roles'))

@app.route('/detalle_orden/<int:id_orden>')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def detalle_orden(id_orden):
    orden = OrdenServicio().consultaIndividual(id_orden)
    return render_template('orden/detalle_orden.html', orden=orden)


'''--------------------------------------------------------------
Rutas para Servicios de Calibración
--------------------------------------------------------------'''

# Listar servicios
@app.route('/servicios')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def listar_servicios():
    servicios = ServicioCalibracion.query.all()
    return render_template('servicio/lista.html', servicios=servicios)

# Agregar servicio
@app.route('/servicios/agregar', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def agregar_servicio():
    clientes = Cliente.query.all()
    equipos = Equipo.query.all()
    if request.method == 'POST':
        nuevo = ServicioCalibracion(
            nombre_servicio=request.form['nombre_servicio'],
            descripcion=request.form['descripcion'],
            costo=request.form['costo'],
            tiempo_estimado=request.form['tiempo_estimado'],
            id_cliente=request.form['id_cliente']
        )
        nuevo.agregar()

        # Asociar equipos seleccionados
        equipos_seleccionados = request.form.getlist('equipos')
        for id_equipo in equipos_seleccionados:
            relacion = ServicioEquipo(id_servicio=nuevo.id_servicio, id_equipo=id_equipo)
            db.session.add(relacion)
        db.session.commit()

        return redirect(url_for('listar_servicios'))
    return render_template('servicio/agregar.html', clientes=clientes, equipos=equipos)

# Editar servicio
@app.route('/servicios/editar/<int:id_servicio>', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def editar_servicio(id_servicio):
    servicio = ServicioCalibracion.query.get(id_servicio)
    clientes = Cliente.query.all()
    equipos = Equipo.query.all()

    if request.method == 'POST':
        # Actualizar datos del servicio
        servicio.nombre_servicio = request.form['nombre_servicio']
        servicio.descripcion = request.form['descripcion']
        servicio.costo = request.form['costo']
        servicio.tiempo_estimado = request.form['tiempo_estimado']
        servicio.id_cliente = request.form['id_cliente']

        # Actualizar equipos asociados
        ServicioEquipo.query.filter_by(id_servicio=id_servicio).delete()
        equipos_seleccionados = request.form.getlist('equipos')
        for id_equipo in equipos_seleccionados:
            relacion = ServicioEquipo(id_servicio=id_servicio, id_equipo=id_equipo)
            db.session.add(relacion)

        # Un solo commit para todo
        db.session.commit()

        return redirect(url_for('listar_servicios'))

    return render_template('servicio/editar.html', servicio=servicio, clientes=clientes, equipos=equipos)

# Eliminar servicio
@app.route('/servicios/eliminar/<int:id_servicio>', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def eliminar_servicio(id_servicio):
    servicio = ServicioCalibracion.query.get(id_servicio)
    servicio.eliminar(id_servicio)
    return redirect(url_for('listar_servicios'))

@app.route('/servicios/detalle/<int:id_servicio>')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder 
def detalle_servicio(id_servicio):
    servicio = ServicioCalibracion.query.get(id_servicio)
    if not servicio:
        return "Servicio no encontrado", 404
    return render_template('servicio/detalle.html', servicio=servicio)

from flask import jsonify

@app.route('/equipos_por_cliente/<int:id_cliente>')
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def equipos_por_cliente(id_cliente):
    equipos = Equipo.query.filter_by(id_cliente=id_cliente).all()
    equipos_data = [
        {"id_equipo": e.id_equipo, "nombre": e.nombre, "marca": e.marca, "modelo": e.modelo}
        for e in equipos
    ]
    return jsonify(equipos_data)


'''--------------------------------------------------------------
Rutas para Detalles de Orden
--------------------------------------------------------------'''
# Listar todas las órdenes (vista general)
@app.route('/detalleorden/ordenes')
@roles_requeridos('administrador', 'supervisor', 'técnico')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def listar_ordenes_detalle():
    ordenes = OrdenServicio.query.all()
    return render_template('detalleorden/ordenes.html', ordenes=ordenes)


# Listar detalles de una orden específica
@app.route('/detalleorden/<int:id_orden>/detalles')
def listar_detalles(id_orden):
    orden = OrdenServicio.query.get(id_orden)
    detalles = DetalleOrden.query.filter_by(id_orden=id_orden).all()
    return render_template('detalleorden/lista.html', orden=orden, detalles=detalles)


# Editar un detalle
@app.route('/detalleorden/<int:id_detalle>/editar', methods=['GET', 'POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def editar_detalle(id_detalle):
    dao = DetalleOrden()  # instancia temporal para usar métodos
    detalle = dao.consultaIndividual(id_detalle)

    if not detalle:
        flash('Detalle no encontrado', 'danger')
        return redirect(url_for('listar_ordenes_detalle'))

    if request.method == 'POST':
        detalle.id_equipo = request.form['id_equipo']
        detalle.id_servicio = request.form['id_servicio']
        detalle.fecha_inicio = request.form['fecha_inicio']
        detalle.fecha_fin = request.form.get('fecha_fin')
        detalle.resultado = request.form.get('resultado')

        detalle.editar()
        flash('Detalle actualizado correctamente', 'success')
        return redirect(url_for('listar_detalles', id_orden=detalle.id_orden))

    equipos = Equipo.query.all()
    servicios = ServicioCalibracion.query.all()
    return render_template('detalleorden/editardetalle.html', detalle=detalle, equipos=equipos, servicios=servicios)

# Rutas para sensor de Temperatura
# Ruta para mostrar lecturas
@app.route('/api/temperatura', methods=['POST'])
@roles_requeridos('administrador', 'supervisor')  # Solo los roles con ID 1 (Administrador) o 2 (Supervisor) pueden acceder
def api_temperatura():
    data = request.get_json()
    nueva = LecturaTemperatura(
        valor=data['valor'],
        dispositivo=data.get('dispositivo', 'ESP32')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"status": "ok", "id": nueva.id})

# Página para visualizar lecturas
@app.route('/iot/temperatura')
def iot_temperatura():
    registros = LecturaTemperatura.query.order_by(LecturaTemperatura.id.desc()).limit(1000).all()
    datos = [r.to_dict() for r in registros]  # convertir a lista de dicts
    return render_template("IoT/Temperatura.html", datos=datos)

#Ruta para la Api movil
from flask import jsonify
@app.route('/api/ordenes', methods=['GET', 'POST'])
def api_ordenes():

    if request.method == 'GET':

        ordenes = OrdenServicio.query.all()

        return jsonify([
            {
                "id": o.id_orden,
                "cliente": o.cliente.nombre_empresa if o.cliente else "N/A",
                "estado": o.estado,
                "fecha": o.fecha_solicitud.strftime("%Y-%m-%d")
            }
            for o in ordenes
        ])

    elif request.method == 'POST':

        data = request.get_json()

        nueva_orden = OrdenServicio(
            fecha_solicitud=data['fecha_solicitud'],
            estado=data['estado'],
            id_cliente=data['id_cliente'],
            id_empleado=data['id_empleado']
        )

        db.session.add(nueva_orden)
        db.session.commit()

        nuevo_detalle = DetalleOrden(
            id_orden=nueva_orden.id_orden,
            id_equipo=data['id_equipo'],
            id_servicio=data['id_servicio'],
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data['fecha_fin'],
            resultado=data['resultado']
        )

        db.session.add(nuevo_detalle)
        db.session.commit()

        return jsonify({
            'mensaje': 'Orden creada correctamente'
        })

@app.route('/api/orden/<int:id>')
def api_orden(id):
    o = OrdenServicio.query.get(id)

    return jsonify({
        "id": o.id_orden,
        "cliente": o.cliente.nombre_empresa if o.cliente else "",
        "estado": o.estado,
        "fecha": o.fecha_solicitud.strftime("%Y-%m-%d")
    })

@app.route('/api/orden/<int:id_orden>/detalle')
def api_detalle_orden(id_orden):

    detalles = DetalleOrden.query.filter_by(id_orden=id_orden).all()

    resultado = []

    for d in detalles:
        resultado.append({
            'id_detalle': d.id_detalle,
            'id_equipo': d.id_equipo,
            'id_servicio': d.id_servicio,
            'fecha_inicio': str(d.fecha_inicio),
            'fecha_fin': str(d.fecha_fin) if d.fecha_fin else None,
            'resultado': d.resultado
        })

    return jsonify(resultado)


    #crear una orden
app. route('/api/orden', methods=['POST'])
def api_crear_orden():
    data = request.get_json()
    nueva_orden = OrdenServicio(
        fecha_solicitud=data['fecha_solicitud'],
        estado=data['estado'],
        id_cliente=data['id_cliente'],
        id_empleado=data['id_empleado']
    )
    db.session.add(nueva_orden)
    db.session.commit()
    return jsonify({"status": "ok", "id": nueva_orden.id_orden})

#Editar Orden desde API
@app.route('/api/orden/<int:id>', methods=['PUT'])
def api_editar_orden(id):
    orden = OrdenServicio.query.get(id)
    if not orden:
        return jsonify({"error": "Orden no encontrada"}), 404

    data = request.get_json()
    orden.fecha_solicitud = data.get('fecha_solicitud', orden.fecha_solicitud)
    orden.estado = data.get('estado', orden.estado)
    orden.id_cliente = data.get('id_cliente', orden.id_cliente)
    orden.id_empleado = data.get('id_empleado', orden.id_empleado)

    db.session.commit()
    return jsonify({"status": "ok"})

#elimianr orden desde API
@app.route('/api/orden/<int:id>/eliminar', methods=['DELETE'])
def api_eliminar_orden(id):
    orden = OrdenServicio.query.get(id)
    if not orden:
        return jsonify({"error": "Orden no encontrada"}), 404

    db.session.delete(orden)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route('/api/servicios')
def api_servicios():

    servicios = ServicioCalibracion.query.all()

    return jsonify([
        {
            'id_servicio': s.id_servicio,
            'nombre_servicio': s.nombre_servicio
        }
        for s in servicios
    ])

@app.route('/api/clientes')
def api_clientes():

    clientes = Cliente.query.all()

    return jsonify([
        {
            'id_cliente': c.id_cliente,
            'nombre_empresa': c.nombre_empresa
        }
        for c in clientes
    ])

@app.route('/api/empleados')
def api_empleados():

    empleados = Empleado.query.all()

    return jsonify([
        {
            'id_empleado': e.id_empleado,
            'nombre': e.nombre
        }
        for e in empleados
    ])


@app.route('/api/equipos')
def api_equipos():

    equipos = Equipo.query.all()

    return jsonify([
        {
            'id_equipo': eq.id_equipo,
            'nombre': eq.nombre,
            'marca': eq.marca,
            'modelo': eq.modelo
        }
        for eq in equipos
    ])

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def api_login():

    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    try:

        data = request.get_json()

        print(data)

        username = data.get('username')
        password = data.get('password')

        usuario = Usuario.query.filter_by(
            username=username,
            activo=True
        ).first()

        if usuario and usuario.check_password(password):

            return jsonify({
                'status': 'ok',
                'usuario': usuario.username,
                'rol': usuario.empleado.rol.nombre
            }), 200

        return jsonify({
            'status': 'error',
            'mensaje': 'Credenciales incorrectas'
        }), 401

    except Exception as e:

        print("ERROR LOGIN:", e)

        return jsonify({
            'status': 'error',
            'mensaje': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

