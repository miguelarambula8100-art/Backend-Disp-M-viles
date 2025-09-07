from flask import Blueprint,request,jsonify
from config.db import get_db_connection

# crear el blueprint
tareas_bp = Blueprint('tareas', __name__)

#Crear un endpoint
@tareas_bp.route('/obtener', methods=['GET'])
def get():
    return jsonify({"mensaje": "esta es la ruta de tareas"})

#Crear endpoint con post recibiendo datos desde el body
@tareas_bp.route('/crear', methods=['POST'])
def crear():

    #Obtener los datos del body 
    data = request.get_json()
    descripcion = data.get('descripcion')
    if not descripcion:
        return jsonify({"error": "Debes teclear una descripción"}),400
    

    #Obtenemos el cursor
    cursor = get_db_connection()
    #Hacemos el insert
    try: 
        cursor.execute('INSERT INTO tareas (descripcion) VALUES(%s)', (descripcion,))
        cursor.connection.commit()
        return jsonify({"message": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"Error": f"No se pudo crear la tarea: {str(e)}"})
    finally:
        #Cierro el cursor y la conexion
        cursor.close()


   
#Crear endpoint usando PUT y pasando datos por el body y el url
@tareas_bp.route('/modificar/<int:user_id>', methods=['PUT'])
def modificar(user_id):

    #Obtenemos los datos del body
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    mensaje = f"Usuario con id: {user_id} y nombre: {nombre} {apellido}"
    
    
    return jsonify({"saludo": mensaje })

