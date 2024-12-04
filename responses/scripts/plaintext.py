import json
import os

responses_folder = "responses"

def get_latest_response_file(responses_folder):
    files = os.listdir(responses_folder)
    latest_file = None
    highest_response_number = -1
    
    for file in files:
        if not file.startswith("response_") or not file.endswith(".json"): continue
        response_number = int(file.split("_")[1])
        if response_number > highest_response_number:
            highest_response_number = response_number
            latest_file = file
    
    return os.path.join(responses_folder, latest_file) if latest_file else None

file_path = get_latest_response_file(responses_folder=responses_folder)

with open(file_path, 'r') as f:
    pr_data = json.load(f)

print(pr_data)

qa_data = pr_data["data"]
questions = list(qa_data.keys())
answers = list(qa_data.values())

output_data = {
    'questions': questions,
    'answers': answers,
    'pr_data': pr_data
}

with open('/tmp/qa_data.json', 'w') as outfile:
    json.dump(output_data, outfile)
