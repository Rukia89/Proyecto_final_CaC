from flask import Flask, jsonify, request
import mysql.connector
import random
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

db_connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='Vv34732453',
    database='biblioteca'
)
cursor = db_connection.cursor()

@app.route('/libros', methods=['GET'])
def get_libros():
    query = "SELECT * FROM libros"
    cursor.execute(query)
    libros = cursor.fetchall()
    libros_list = []
    for libro in libros:
        libros_list.append({
            'id': libro[0],
            'titulo': libro[1],
            'autor': libro[2],
            'genero': libro[3],
            'disponible': libro[4]
        })
    return jsonify(libros_list)

@app.route('/libros', methods=['POST'])
def add_libro():
    datos = request.get_json()
    titulo = datos['titulo']
    autor = datos['autor']
    genero = datos.get('genero')
    disponible = True  

    query = "INSERT INTO libros (titulo, autor, genero, disponible) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (titulo, autor, genero, disponible))
    db_connection.commit()

    return 'Libro registrado correctamente', 201

@app.route('/libros/<int:id>', methods=['PUT'])
def update_libro(id):
    datos = request.get_json()
    titulo = datos.get('titulo')
    autor = datos.get('autor')
    genero = datos.get('genero')

    query = "UPDATE libros SET titulo=%s, autor=%s, genero=%s WHERE id=%s"
    cursor.execute(query, (titulo, autor, genero, id))
    db_connection.commit()

    return 'Libro actualizado correctamente', 200

@app.route('/libros/<int:id>', methods=['DELETE'])
def delete_libro(id):
    query = "DELETE FROM libros WHERE id=%s"
    cursor.execute(query, (id,))
    db_connection.commit()

    return 'Libro eliminado correctamente', 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario[0],
            'nombre': usuario[1],
            'email': usuario[2],
            'telefono': usuario[3]
        })
    return jsonify(usuarios_list)

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    datos = request.get_json()
    nombre = datos['nombre']
    email = datos['email']
    telefono = datos.get('telefono')

    query = "INSERT INTO usuarios (nombre, email, telefono) VALUES (%s, %s, %s)"
    cursor.execute(query, (nombre, email, telefono))
    db_connection.commit()

    return 'Usuario registrado correctamente', 201

@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    datos = request.get_json()
    nombre = datos.get('nombre')
    email = datos.get('email')
    telefono = datos.get('telefono')

    query = "UPDATE usuarios SET nombre=%s, email=%s, telefono=%s WHERE id=%s"
    cursor.execute(query, (nombre, email, telefono, id))
    db_connection.commit()

    return 'Usuario actualizado correctamente', 200

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    query = "DELETE FROM usuarios WHERE id=%s"
    cursor.execute(query, (id,))
    db_connection.commit()

    return 'Usuario eliminado correctamente', 200

@app.route('/prestamos', methods=['GET'])
def get_prestamos():
    query = "SELECT * FROM prestamos"
    cursor.execute(query)
    prestamos = cursor.fetchall()
    prestamos_list = []
    for prestamo in prestamos:
        prestamos_list.append({
            'id': prestamo[0],
            'id_libro': prestamo[1],
            'id_usuario': prestamo[2],
            'fecha_prestamo': prestamo[3].strftime('%Y-%m-%d'),
            'fecha_devolucion': prestamo[4].strftime('%Y-%m-%d'),
            'dias_prestamo': prestamo[5]
        })
    return jsonify(prestamos_list)

@app.route('/prestamos', methods=['POST'])
def add_prestamo():
    datos = request.get_json()
    id_libro = datos['id_libro']
    id_usuario = datos['id_usuario']
    fecha_prestamo = datos['fecha_prestamo']
    fecha_devolucion = datos['fecha_devolucion']
    dias_prestamo = datos['dias_prestamo']

    query = "INSERT INTO prestamos (id_libro, id_usuario, fecha_prestamo, fecha_devolucion, dias_prestamo) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (id_libro, id_usuario, fecha_prestamo, fecha_devolucion, dias_prestamo))
    db_connection.commit()

    return 'Préstamo registrado correctamente', 201

@app.route('/prestamos/<int:id>', methods=['DELETE'])
def delete_prestamo(id):
    query = "DELETE FROM prestamos WHERE id=%s"
    cursor.execute(query, (id,))
    db_connection.commit()

    return 'Préstamo eliminado correctamente', 200

@app.route('/titulo-aleatorio', methods=['GET'])
def obtener_titulo_aleatorio():
    titulos_aleatorios = [
        "La sombra del viento",
        "Cien años de soledad",
        "El código Da Vinci",
        "El principito",
        "1984",
        "Orgullo y prejuicio",
        "El señor de los anillos",
        "Don Quijote de la Mancha",
        "Harry Potter y la piedra filosofal",
        "Matar a un ruiseñor"
    ]
    titulo = random.choice(titulos_aleatorios)
    return jsonify({'titulo': titulo})

if __name__ == '__main__':
    app.run(debug=True)
