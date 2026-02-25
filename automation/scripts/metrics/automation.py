import requests
import csv
from datetime import datetime
import os
import urllib3

# Suppress SSL warnings for self-signed certificates (common in Proxmox)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
PROXMOX_IP = "10.8.0.16"  # Node 1 IP (Nested Proxmox)
NODE_NAME = "node1"
VM_ID = "100"
TOKEN_ID = "root@pam!automation"
TOKEN_SECRET = "7850c8d4-a715-48c5-b94e-f100ec5b49b0"

# API Endpoints
BASE_URL = f"https://{PROXMOX_IP}:8006/api2/json/nodes/{NODE_NAME}/qemu/{VM_ID}"
HEADERS = {"Authorization": f"PVEAPIToken={TOKEN_ID}={TOKEN_SECRET}"}

def fetch_vm_metrics():
    """
    Fetches both status and configuration data from Proxmox API
    and merges them into a single dictionary.
    """
    try:
        # Request current status (CPU, RAM, Net usage)
        status_res = requests.get(f"{BASE_URL}/status/current", headers=HEADERS, verify=False, timeout=10)
        # Request VM configuration (Assigned RAM, Cores, Name)
        config_res = requests.get(f"{BASE_URL}/config", headers=HEADERS, verify=False, timeout=10)

        if status_res.status_code == 200 and config_res.status_code == 200:
            status_data = status_res.json().get('data', {})
            config_data = config_res.json().get('data', {})

            # Merge status and config dictionaries
            combined_metrics = {**status_data, **config_data}

            # Add timestamp at the beginning of the record
            now = datetime.now()
            final_record = {
                'Date': now.strftime("%Y-%m-%d"),
                'Time': now.strftime("%H:%M:%S")
            }
            final_record.update(combined_metrics)
            return final_record
        else:
            print(f"[{datetime.now()}] API Error: Status {status_res.status_code}, Config {config_res.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Connection Failed: {e}")
    return None

def save_metrics_to_csv(data, filename="/home/drosos/vm_metrics.csv"):
    """
    Appends the gathered metrics to a CSV file.
    Writes the header only if the file is being created for the first time.
    """
    file_exists = os.path.isfile(filename)

    # Use keys from the data as field names (columns)
    fieldnames = list(data.keys())

    with open(filename, mode='a', newline='') as csvfile:
        # extrasaction='ignore' ensures the script doesn't crash if new API fields appear
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

if __name__ == "__main__":
    # Main execution block
    metrics = fetch_vm_metrics()
    if metrics:
        save_metrics_to_csv(metrics)
        print(f"[{datetime.now()}] Success: Data saved to CSV.")
    else:
        print(f"[{datetime.now()}] Failure: Could not retrieve metrics.")