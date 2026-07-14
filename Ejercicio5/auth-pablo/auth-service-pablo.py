from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import timedelta

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "123456")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

def get_connection():
    return mysql.connector.connect(
        host = os.environ.get("MYSQL_HOST", "mysql-service"),
        user = os.environ.get("MYSQL_USER", "root"),
        password = os.environ.get("MYSQL_PASSWORD", "password"),
        database = os.environ.get("MYSQL_DB", "auth_db")
        )

@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user["password"], password):
            access_token = create_access_token(
                identity = user ["id"],
                additional_claims = {"username", user["username"]}
            )
            return jsonify({
                "access_token": access_token,
                "user_id": user["id"],
                "username": user["username"]
            })
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals():
            conn.close()
    
@app.route("/auth/validate", methods=["POST"])
@jwt_required()
def validar():
    try:
        current_user_id = get_jwt_identity()
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, username FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"valid": True, "user_id": user["id"], "username": user["username"]})
        return jsonify({"valid": False}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals():
            conn.close()

@app.route("/auth/register", methods=["POST"])
def registro():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "El usuario ya existe, ingrese otro"}), 409
        
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return jsonify({"message", "Usuario ingresado correctamente"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if "conn" in locals():
            conn.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"auth_service_status": "healthy"})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    