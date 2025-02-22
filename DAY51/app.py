from flask import Flask, jsonify, request, render_template
import threading
import time

app = Flask(__name__)

pet = {
    "name": "Zoa",
    "hunger": 50,      
    "happiness": 50    
}

def pet_decay():
    while True:
        time.sleep(60)  
        pet["hunger"] = min(100, pet["hunger"] + 2)
        pet["happiness"] = max(0, pet["happiness"] - 1)

threading.Thread(target=pet_decay, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def status():
    return jsonify(pet)

@app.route("/feed", methods=["POST"])
def feed():
    pet["hunger"] = max(0, pet["hunger"] - 10)
    pet["happiness"] = min(100, pet["happiness"] + 5)
    return jsonify(pet)

@app.route("/play", methods=["POST"])
def play():
    pet["happiness"] = min(100, pet["happiness"] + 10)
    pet["hunger"] = min(100, pet["hunger"] + 5)
    return jsonify(pet)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
