from flask import Flask, jsonify
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

@app.route("/health", methods=["GET"])
def health_check():
    db = get_db()
    if db is None:
        return jsonify({"status": "error", "message": "Error de conexión con la BDD"}), 500
    return jsonify({"status": "ok"}), 200

@app.route("/products", methods=["GET"])
def obtener_productos():
    try:
        db = get_db()
        if db is None:
            return jsonify({"status": "error", "message": "Error de conexión con MongoDB"}), 500
        productos = list(db[MONGO_COLLECTION].find({}, {"_id":0}))
        
        if productos is None:
            return jsonify({"status": "ok", "productos": []}), 200
        
        return jsonify({"status": "ok", "productos": productos}), 200
    except Exception as e:
        logger.error(f"Error al obtener los productos: {e}")
        return jsonify({"error": "Error al obtener productos"}), 500
    
@app.route("/products/<nombre>", methods=['GET'])
def obtener_producto_nombre(nombre):
    try:
        db = get_db()
        if db is None:
            return jsonify({"status": "error", "message": "Error de conexión con MongoDB"}), 500
        producto = db[MONGO_COLLECTION].find_one({"nombre": nombre}, {"_id":0})        
        if producto is None:
            return jsonify({"status": "ok", "producto": None}), 200
        
        return jsonify({"status": "ok", "producto": producto}), 200
    except Exception as e:
        logger.error(f"Error al obtener el producto: {e}")
        return jsonify({"error": "Error al obtener producto"}), 500        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)