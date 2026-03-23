from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    user = User.query.filter_by(nombre=data['nombre']).first()

    if not user:
        return jsonify({"error": "Usario no existe"}), 404
    
    token = create_access_token(identity=str(user.id))

    return jsonify(token=token)

@app.route('/')
def home():
    return "Hola Mundo"

@app.route('/users')
@jwt_required()
def get_users():
    users = User.query.all()

    resultado = []

    for user in users:
        resultado.append({
            "id": user.id,
            "nombre": user.nombre
        })
    return jsonify(resultado)

@app.route('/users', methods=['POST'])
@jwt_required()
def create_users():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    if "nombre" not in data:
        return jsonify({"error": "Falta  nombre"}), 400 

    nuevo_usuario = User(nombre=data["nombre"])

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre
    
    }), 201

@app.route('/users/<int:id>')
@jwt_required()
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "Usario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "nombre": user.nombre
    })

@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_users(id):
    data = request.get_json()

    if not data: 
        return jsonify({"error": "No data"}), 400

    user = User.query.get(id)

    if not user:
        return jsonify({"error": "Usario no encontrado"}), 404

    user.nombre = data["nombre"]

    db.commit()

    return jsonify({
        "id": user.id,
        "nombre": user.nombre
    })

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_users(id):

    user = User.query.get(id)

    if not user:
        return jsonify({"error": "Usario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"Message": f"El usario {id} ha sido eliminado"})

if __name__ == '__main__':
    app.run(debug=True)

