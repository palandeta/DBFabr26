from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb-service:27017")
MONGO_DB = os.environ.get("MONGO_DB", "productosdb")
MONGO_COLLECTION = os.environ.get ("MONGO_COLLECTION", "products")

def get_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        logger.info(f"Conectado a la DB de MongoDB: {MONGO_URI}")
        return db
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {e}")
        return None

@app.route("/healthpost", methods=["GET"])
def health_check():
    db = get_db()
    if db is None:
        return jsonify({"status": "error", "message": "Error de conexión con la BDD"}), 500
    return jsonify({"status": "ok"}), 200

@app.route("/postproduct", methods=["POST"])
def crear_producto():
    try:
        data = request.json
        if not data or "nombre" not in data or "precio" not in data:
            return jsonify({"error": "Se requieren los campos nombre y precio"}), 400
        
        nombre = data["nombre"]
        precio = data["precio"]
        
        db = get_db()
        if db is None:
            return jsonify({"status": "error", "message": "Error de conexión con MongoDB"}), 500
        
        producto = {
            "nombre": nombre,
            "precio": precio
        }
        
        result = db[MONGO_COLLECTION].insert_one(producto)
        
        return jsonify({"status": "ok", 
                        "mensaje": "Producto insertado correctamente",
                        "producto": {"nombre": nombre,"precio": precio},
                        "id": str(result.inserted_id)}), 201
    except Exception as e:
        logger.error(f"Error al crear el producto: {e}")
        return jsonify({"error": "Error al insertar producto"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)