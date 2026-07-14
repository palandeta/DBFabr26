from flask import Flask, request, jsonify, redirect
import requests
import os

app = Flask(__name__)

url_auth = os.environ.get("AUTH_SERVICE_HOST", "auth-service-pablo")
AUTH_SERVICE_URL = f"http://{url_auth}:5000"

@app.route("/api/auth/<path:path>", methods= ['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(path):
    try:
        url = f"{AUTH_SERVICE_URL}/auth/{path}"
        
        response = requests.request(
            method = request.method,
            url = url,
            headers = {key: value for key, value in request.headers if key != 'Host'},
            data = request.get_data(),
            cookies = request.cookies,
            allow_redirects = False
            )
        
        return response.content, response.status_code, response.headers.items()
    except Exception as e:
        return jsonify({"error": f'Gateway error: {str(e)}' }), 500

@app.route('/healthgw', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "api-gateway-pablo"})

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "El API Gateway se esta ejecutando", "endpoints": {"auth": "/api/auth/*"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5002, debug=True)