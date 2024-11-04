from flask import Flask, jsonify, request
import psutil
import subprocess
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "12345"  
jwt = JWTManager(app)

# Endpoint de autenticación
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    # Aquí se validaría el usuario y contraseña 
    if username == "admin" and password == "password":  
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

# Endpoint para el uso de dispositivos
@app.route("/device-usage", methods=["GET"])
@jwt_required()
def device_usage():
    device_name = request.args.get("device_name")
    if device_name:
        try:
            usage = psutil.disk_usage(f"/dev/{device_name}")
            return jsonify({
                "device": device_name,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except FileNotFoundError:
            return jsonify({"error": f"Device {device_name} not found"}), 404
    else:
        devices_usage = []
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            devices_usage.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        return jsonify(devices_usage)

# Endpoint para ejecutar un script
@app.route("/run-script", methods=["POST"])
@jwt_required()
def run_script():
    try:
        output = subprocess.check_output(["/app/script.sh"], stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e), "output": e.output}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
