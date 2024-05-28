from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pymysql import connect

app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Frutillita12@localhost:3306/apartaguest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelado de las tablas
class apartamentos(db.Model):
    __tablename__ = 'apartamentos'
    id_apartamento = db.Column(db.Integer, primary_key=True)
    nombre_edificio = db.Column(db.String(255), nullable=False)
    numero_apartamento = db.Column(db.Integer, nullable=False)
    piso = db.Column(db.Integer, nullable=False)
    tamaño = db.Column(db.Integer, nullable=False)
    precio_alquiler = db.Column(db.Numeric(10, 2), nullable=False)
    disponibilidad = db.Column(db.Enum('Disponible', 'No Disponible'), nullable=False)
    clasificaciones = db.relationship('ClasificacionApartamentos', backref='apartamento', lazy=True)
    inquilinos = db.relationship('Inquilinos', backref='apartamento', lazy=True)
    contratos = db.relationship('Contratos', backref='apartamento', lazy=True)
                                
class ClasificacionApartamentos(db.Model):
    __tablename__ = 'clasificacion_apartamentos'
    id_clasificacion = db.Column(db.Integer, primary_key=True)
    nombre_clasificacion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    id_apartamento = db.Column(db.Integer, db.ForeignKey('apartamentos.id_apartamento'), nullable=False)

class Inquilinos(db.Model):
    __tablename__ = 'inquilinos'
    id_inquilino = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    correo_electronico = db.Column(db.String(255), nullable=False)
    id_apartamento = db.Column(db.Integer, db.ForeignKey('apartamentos.id_apartamento'), nullable=False)
    contratos = db.relationship('Contratos', backref='inquilino', lazy=True)

class Contratos(db.Model):
    __tablename__ = 'contratos'
    id_contrato = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    id_inquilino = db.Column(db.Integer, db.ForeignKey('inquilinos.id_inquilino'), nullable=False)
    id_apartamento = db.Column(db.Integer, db.ForeignKey('apartamentos.id_apartamento'), nullable=False)
    pagos = db.relationship('Pagos', backref='contrato', lazy=True)

class Pagos(db.Model):
    __tablename__ = 'pagos'
    id_pago = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    tipo_pago = db.Column(db.Enum('Efectivo', 'Tarjeta', 'Transferencia'), nullable=False)
    id_contrato = db.Column(db.Integer, db.ForeignKey('contratos.id_contrato'), nullable=False)

