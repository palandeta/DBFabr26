from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/prodpablo", methods=["GET"])

def get_products():
    products = [
        {"id":1, "name": "cuadernos", "price": 3.00},
        {"id":2, "name": "lapices", "price": 0.80},
        {"id":3, "name": "esferos", "price": 1.00}
        ]
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)