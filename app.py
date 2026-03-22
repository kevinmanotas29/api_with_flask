from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "nombre": "Kevin"},
    {"id": 2, "nombre": "Atom"}
]

@app.route('/')
def home():
    return "Hola Mundo"

@app.route('/users')
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_users():
    nuevo_usuario = request.get_json()

    if not nuevo_usuario:
        return jsonify({"error": "no data"}), 400

    if "nombre" not in nuevo_usuario:
        return jsonify({"error": "Falta  nombre"}), 400 

    nuevo_usuario ["id"] = len(users) + 1
    users.append(nuevo_usuario)
    return jsonify(nuevo_usuario), 200

@app.route('/users/<int:id>')
def get_user(id):
    for user in users:
        if user ["id"] == id:
            return jsonify(user)
    return jsonify({"error": "Usario no encontrado"}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_users(id):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return jsonify({"message": f"El user {id} ha sido eliminado"})
    return jsonify({"error": "User no encontrado"}), 404

@app.route('/users/<int:id>', methods=['PUT'])
def update_users(id):
    data = request.get_json()

    if not data: 
        return jsonify({"error": "No data"}), 400


    for user in users:
        if user["id"] == id:
            user ["nombre"] = data["nombre"]
            return jsonify({"Message": "Un nuevo usario ha sido actulizado"})

    return jsonify({"Error": "Usuario no encontrado"}), 404


if __name__ == '__main__':
    app.run()

