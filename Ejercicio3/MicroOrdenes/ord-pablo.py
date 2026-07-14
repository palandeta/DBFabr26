from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/ordpablo", methods=["GET"])

def get_orders():
    orders = [
        {"id":1, "name": "Juan", "value": 3.00, "city": "Ibarra"},
        {"id":2, "name": "Luis", "value": 0.80, "city": "Quito"},
        {"id":3, "name": "Pedro", "value": 1.00, "city": "Ambato"}
        ]
    return jsonify(orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)