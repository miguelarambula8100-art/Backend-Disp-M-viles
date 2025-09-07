from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import Bcrypt

from config.db import get_db_connection

import os
from dotenv import load_dotenv

#Cargamos las variables de entorno
load_dotenv()

#Creamos el Blueprint 
usuarios_bp = Blueprint('usuarios', __name__)

#Inicializar Bcrypt
bcrypt = Bcrypt()

@usuarios_bp.route('/registrar', methods=['POST'])
def registar():
    #obtener del body los datos
    data = request.get_json()
    
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    #Validacion
    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400
    
    #Obtener el cursor de la BD
    cursor = get_db_connection()

    try:
        #Verificamos que el usuario no exista
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"error": "Este usuario no existe"}), 400
        #HAcemos hash al password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #Insertar el registro en la nueva base de datos
        cursor.execute(''' INSERT into usuarios (nombre, email, password) values (%s, %s, %s)''', 
                       (nombre, email, hashed_password))
        
        #guardamos el nuevo registro
        cursor.connection.commit()

        return jsonify({"mensaje": "El usuario se creo correctamente"}), 201
    

    except Exception as e:
        return jsonify({"error":f"Error al registrar el usuario: {str(e)}"}), 500

    finally:
        cursor.close()

        
@usuarios_bp.route('/login', methods=['POST'])
def login():

    data = request .json()

    email=data.get('email')
    password=data.get('password')

    if not email or not password:
        return jsonify({"error": "Faltan Datos perro"}), 400
    cursor = get_db_connection()
    
    #cursor.execute("SELECT : ")    