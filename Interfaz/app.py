from flask import Flask, render_template, request, url_for, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from sqlalchemy import Column, Integer, String, Enum, Numeric, Date, ForeignKey
from pymysql import connect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Ñoño_123'

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Estrellita20.@localhost:3306/apartaguest'
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
    #disponibilidad = db.Column(Enum('Disponible', 'No Disponible', name='disponibilidad_enum'), nullable=False)
    clasificaciones = db.relationship('clasificacionapartamentos', backref='apartamento', lazy=True)
    inquilinos = db.relationship('inquilinos', backref='apartamento', lazy=True)
    contratos = db.relationship('contratos', backref='apartamento', lazy=True)
                                
class clasificacionapartamentos(db.Model):
    __tablename__ = 'clasificacion_apartamentos'
    id_clasificacion = db.Column(db.Integer, primary_key=True)
    nombre_clasificacion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    id_apartamento = db.Column(db.Integer, db.ForeignKey('apartamentos.id_apartamento'), nullable=False)

class inquilinos(db.Model):
    __tablename__ = 'inquilinos'
    id_inquilino = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    correo_electronico = db.Column(db.String(255), nullable=False)
    id_apartamento = db.Column(db.Integer, db.ForeignKey('apartamentos.id_apartamento'), nullable=False)
    contratos = db.relationship('contratos', backref='inquilino', lazy=True)

class contratos(db.Model):
    __tablename__ = 'contratos'
    id_contrato = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    id_inquilino = db.Column(db.Integer, db.ForeignKey('inquilinos.id_inquilino'), nullable=False)
    id_apartamento = db.Column(db.Integer, db.ForeignKey('apartamentos.id_apartamento'), nullable=False)
    pagos = db.relationship('pagos', backref='contrato', lazy=True)

class pagos(db.Model):
    __tablename__ = 'pagos'
    id_pago = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    tipo_pago = db.Column(Enum('Efectivo', 'Tarjeta', 'Transferencia', name='tipo_pago_enum'), nullable=False)
    id_contrato = db.Column(db.Integer, db.ForeignKey('contratos.id_contrato'), nullable=False)

class usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id_usuarios = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contra = db.Column(db.String(250), nullable=False)

    # Encriptar contraseña
    def set_password(self, password):
        self.contra = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contra, password)

#
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contra = request.form['contra']

        # Verificar el usuario en la base de datos
        usuario = usuarios.query.filter_by(nombre=nombre).first()
        if usuario is not None and usuario.check_password(contra):
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/Ir_registrarse')
def Ir_registrarse():
    return render_template('registrarse.html')

@app.route('/registrarse', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre_reg']
        contra = request.form['contra_reg']

        # Verificar si el usuario ya existe
        if usuarios.query.filter_by(nombre=nombre).first() is not None:
            flash('El nombre de usuario ya está en uso.')
            return redirect(url_for('register'))

        # Crear un nuevo usuario y cifrar su contraseña
        nuevo_usuario = usuarios(nombre=nombre)
        nuevo_usuario.set_password(contra)

        # Añadir el nuevo usuario a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario creado con éxito. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('registrarse.html')


if __name__ == '__main__':
    app.run(debug=True)