from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from pymysql import connect

app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Frutillita12@localhost:3306/apartaguest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelado de las tablas
class apartamento(db.Model):
    id_inquilino = db.Column(db.Integer, primary_key=True)
    nombre_edificio = db.Column(db.String(255), nullable=False)
    numero_apartamento = db.Column(db.Integer, unique=True, nullable=False)
    piso = db.Column(db.Integer, nullable=False)
    tamaño = db.Column(db.Integer, nullable=False)
    precio_alquiler = db.Column(db.Double(10,2), nullable=False)
    disponibilidad = db.Column(db.Column(Enum('Disponible', 'Ocupado', 'Reservado', name='estado_enum'), nullable=False))