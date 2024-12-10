import json
import os
import sys

responses_folder = "responses"

from datetime import datetime

def get_latest_response_file(responses_folder):
    files = os.listdir(responses_folder)
    latest_file = None
    latest_timestamp = None
    
    for file in files:
        if not file.startswith("response_") or not file.endswith(".json"): 
            continue
        
        try:
            full_path = os.path.join(responses_folder, file)
            with open(full_path, 'r') as f:
                data = json.load(f)
            current_timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            if latest_timestamp is None or current_timestamp > latest_timestamp:
                latest_timestamp = current_timestamp
                latest_file = file
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Skipping file {file} due to error: {e}")
            continue
    return os.path.join(responses_folder, latest_file) if latest_file else None

file_path = get_latest_response_file(responses_folder=responses_folder)

with open(file_path, 'r') as f:
    pr_data = json.load(f)

sys.exit(0 if pr_data["email"].endswith(".ac.in") else 1)