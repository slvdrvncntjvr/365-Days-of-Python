import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
API_URL = 'https://www.virustotal.com/api/v3/ip_addresses/'


ip_addresses = [
"""put your ip addresses here"""
]

def check_ip(ip):
    headers = {
        "x-apikey": API_KEY
    }
    url = API_URL + ip
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"IP {ip}: {data['data']['attributes']['last_analysis_stats']}")
    else:
        print(f"Error fetching data for {ip}: {response.status_code}")

for ip in ip_addresses:
    check_ip(ip)
    time.sleep(15)  