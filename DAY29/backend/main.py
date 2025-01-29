from fastapi import FastAPI
import random
import json
from datetime import datetime

app = FastAPI()

with open("data/world_map.geojson") as f:
    world_map = json.load(f)


ATTACK_TYPES = ["DDoS", "Phishing", "Ransomware", "Malware Injection", "SQL Injection"]

attack_log = []

@app.get("/")
def home():
    return {"message": "Welcome to CyberRisk Analyzer!"}

@app.get("/simulate_attack")
def simulate_attack():
    country = random.choice(world_map["features"])["properties"]["ADMIN"]
    attack_type = random.choice(ATTACK_TYPES)
    timestamp = datetime.now().isoformat()

    attack = {
        "country": country,
        "attack_type": attack_type,
        "timestamp": timestamp
    }
    attack_log.append(attack)

    return attack

@app.get("/attack_logs")
def get_logs():
    return attack_log
