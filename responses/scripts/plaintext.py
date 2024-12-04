import json
import os

file_path = os.getenv('GITHUB_EVENT_PATH')
with open(file_path, 'r') as f:
    pr_data = json.load(f)

qa_data = pr_data['data']
questions = list(qa_data.keys())
answers = list(qa_data.values())

output_data = {
    'questions': questions,
    'answers': answers,
    'pr_data': pr_data
}

with open('/tmp/qa_data.json', 'w') as outfile:
    json.dump(output_data, outfile)