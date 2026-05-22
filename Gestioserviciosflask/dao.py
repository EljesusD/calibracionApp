
# Modelo del sistema de gestión de servicios de calibración

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL, Boolean, Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

'''--------------------------------------------------------------
usuarios y autenticacion
-------------------------------------------------------------'''
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleado.id_empleado'), nullable=False)

    empleado = db.relationship("Empleado", back_populates="usuario")

    # Métodos para manejar contraseñas
    def set_password(self, password):
        """Genera el hash seguro de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña contra el hash almacenado"""
        return check_password_hash(self.password_hash, password)

'''--------------------------------------------------------------
Funcionalidades para Equipos    
--------------------------------------------------------------'''
class Equipo(db.Model):
    __tablename__ = 'Equipo'
    id_equipo = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    marca = Column(String(100))
    modelo = Column(String(100))
    numero_serie = Column(String(100))
    rango_medicion = Column(String(100))
    resolucion = Column(String(100))
    id_cliente = Column(Integer, ForeignKey('Cliente.id_cliente'), nullable=False)

    cliente = relationship("Cliente", back_populates="equipos") 
    servicios = relationship("ServicioCalibracion", secondary="ServicioEquipo", back_populates="equipos")
    detalles = relationship("DetalleOrden", back_populates="equipo")
    
    # Métodos CRUD estilo DAO
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Equipo.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        equipo = self.consultaIndividual(id)
        db.session.delete(equipo)
        db.session.commit()

    def eliminacionLogica(self, id):
        equipo = self.consultaIndividual(id)
        equipo.resolucion = "Inactivo"  # ejemplo de campo para marcar estado
        equipo.editar()


'''--------------------------------------------------------------
Funcionalidades para Clientes 
--------------------------------------------------------------'''
class Cliente(db.Model):
    __tablename__ = 'Cliente'
    id_cliente = Column(Integer, primary_key=True)
    nombre_empresa = Column(String(150), nullable=False)
    contacto = Column(String(150))
    telefono = Column(String(20))
    correo = Column(String(150))
    direccion = Column(String(200))

    equipos = relationship("Equipo", back_populates="cliente")
    ordenes = relationship("OrdenServicio", back_populates="cliente")
    servicios = relationship("ServicioCalibracion", back_populates="cliente")


    # Métodos CRUD estilo DAO
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Cliente.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        cliente = self.consultaIndividual(id)
        db.session.delete(cliente)
        db.session.commit()


'''--------------------------------------------------------------
Funcionalidades para Ordenes de Servicio
--------------------------------------------------------------'''

class OrdenServicio(db.Model):
    __tablename__ = 'OrdenServicio'
    id_orden = Column(Integer, primary_key=True)
    fecha_solicitud = Column(Date, nullable=False)
    estado = Column(String(50), default="Pendiente")
    id_cliente = Column(Integer, ForeignKey('Cliente.id_cliente'), nullable=False)
    id_empleado = Column(Integer, ForeignKey('Empleado.id_empleado'))

    cliente = relationship("Cliente", back_populates="ordenes")
    empleado = relationship("Empleado", back_populates="ordenes")
    detalles = relationship("DetalleOrden", back_populates="orden")


    # Métodos CRUD
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return OrdenServicio.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        orden = self.consultaIndividual(id)
        db.session.delete(orden)
        db.session.commit()


'''--------------------------------------------------------------
Funcionalidades para Empleados ok
--------------------------------------------------------------'''

class Empleado(db.Model):
    __tablename__ = 'Empleado'
    id_empleado = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(150), nullable=False)
    correo = Column(String(150))
    telefono = Column(String(20))
    direccion = Column(String(200))
    escolaridad = Column(String(100))
    id_rol = Column(Integer, ForeignKey('Rol.id_rol'))

    rol = relationship("Rol", back_populates="empleados")
    ordenes = relationship("OrdenServicio", back_populates="empleado")
    usuario = relationship("Usuario", uselist=False, back_populates="empleado")  # relación uno a uno

    # Métodos CRUD
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Empleado.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        empleado = self.consultaIndividual(id)
        db.session.delete(empleado)
        db.session.commit()


'''--------------------------------------------------------------
Funcionalidades para Roles revisado y corregido
--------------------------------------------------------------'''
class Rol(db.Model):
    __tablename__ = 'Rol'
    id_rol = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))

    empleados = relationship("Empleado", back_populates="rol")


    # Métodos CRUD
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Rol.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        rol = self.consultaIndividual(id)
        db.session.delete(rol)
        db.session.commit()

'''--------------------------------------------------------------
servicio de calibracion
--------------------------------------------------------------'''


class ServicioCalibracion(db.Model):
    __tablename__ = 'ServicioCalibracion'
    id_servicio = Column(Integer, primary_key=True)
    nombre_servicio = Column(String(150), nullable=False)
    descripcion = Column(String(255))
    costo = Column(DECIMAL(10, 2))
    tiempo_estimado = Column(Integer)
    id_cliente = Column(Integer, ForeignKey('Cliente.id_cliente'), nullable=False)

    cliente = relationship("Cliente", back_populates="servicios")
    equipos = relationship("Equipo", secondary="ServicioEquipo", back_populates="servicios")
    detalles = relationship("DetalleOrden", back_populates="servicio")


    # Métodos CRUD estilo DAO
    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return ServicioCalibracion.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        servicio = self.consultaIndividual(id)
        db.session.delete(servicio)
        db.session.commit()

class ServicioEquipo(db.Model):
    __tablename__ = 'ServicioEquipo'
    id_servicio_equipo = Column(Integer, primary_key=True)
    id_servicio = Column(Integer, ForeignKey('ServicioCalibracion.id_servicio'), nullable=False)
    id_equipo = Column(Integer, ForeignKey('Equipo.id_equipo'), nullable=False)




'''--------------------------------------------------------------
detalle de orden de servicio
--------------------------------------------------------------'''

class DetalleOrden(db.Model):
    __tablename__ = 'DetalleOrden'

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_orden = Column(Integer, ForeignKey('OrdenServicio.id_orden'), nullable=False)
    id_equipo = Column(Integer, ForeignKey('Equipo.id_equipo'), nullable=False)
    id_servicio = Column(Integer, ForeignKey('ServicioCalibracion.id_servicio'), nullable=False)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    resultado = Column(String(1000))

    # Relaciones
    orden = relationship("OrdenServicio", back_populates="detalles")
    equipo = relationship("Equipo", back_populates="detalles")
    servicio = relationship("ServicioCalibracion", back_populates="detalles")

    # Métodos CRUD estilo DAO (funciones normales)
    def consultaGeneral(self):
        return DetalleOrden.query.all()

    def consultaIndividual(self, id):
        return DetalleOrden.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        detalle = self.consultaIndividual(id)
        db.session.delete(detalle)
        db.session.commit()


# Modelo de la tabla
class LecturaTemperatura(db.Model):
    __tablename__ = 'lecturas_temperatura'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    valor = db.Column(db.Float, nullable=False)
    dispositivo = db.Column(db.String(50), default="ESP32")

    def to_dict(self):
        return {
            "id": self.id,
            # Formato legible: Año-Mes-Día Hora:Minuto:Segundo
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "valor": self.valor,
            "dispositivo": self.dispositivo
        }






'''--------------------------------------------------------------
certificado de calibracion
--------------------------------------------------------------'''
