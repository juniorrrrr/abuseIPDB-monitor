import requests
from ipaddress import ip_network
import time
import json

# Configurations
ABUSEIPDB_API_KEY = "your_abuseipdb_api_key"
PUSHOVER_USER_KEY = "your_pushover_user_key"
PUSHOVER_API_TOKEN = "your_pushover_app_token"
NOTIFIED_IPS_FILE = "/root/notified_ips.json"  # Path to store notified IPs with scores

# IP blocks to monitor
BLOCKS = [
    "192.168.0.0/24",
    "10.0.0.0/24"
]

# Function to check IPs on AbuseIPDB
def check_ip_abuse(ip):
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']['abuseConfidenceScore']
    return 0

# Function to expand CIDR block into individual IPs
def expand_cidr(cidr):
    return [str(ip) for ip in ip_network(cidr)]

# Function to send notification via Pushover
def send_pushover_notification(ip, score):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": f"The IP {ip} has been listed on AbuseIPDB with a score of {score}.",
        "title": "AbuseIPDB Alert"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Error sending Pushover notification: {response.text}")

# Function to load previously notified IPs with scores
def load_notified_ips():
    try:
        with open(NOTIFIED_IPS_FILE, "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save notified IPs with scores
def save_notified_ips(data):
    with open(NOTIFIED_IPS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Execute the check
if __name__ == "__main__":
    print("Starting IP monitoring...")
    notified_ips = load_notified_ips()
    for block in BLOCKS:
        print(f"Checking block: {block}")
        ips = expand_cidr(block)
        for ip in ips:
            current_score = check_ip_abuse(ip)
            if current_score > 0:
                previous_score = notified_ips.get(ip, 0)
                if current_score > previous_score:
                    print(f"Alert: {ip} listed with new score {current_score}.")
                    send_pushover_notification(ip, current_score)
                    notified_ips[ip] = current_score
            time.sleep(1)  # Avoid exceeding API request limits
    save_notified_ips(notified_ips)
    print("Monitoring completed.")
