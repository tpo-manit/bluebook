import json
import os
import ollama

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

if not pr_data["email"].endswith(".ac.in"):
    moderation_output = "No, Unauthorized Email."
    with open('/tmp/moderation_result.txt', 'w') as result_file:
        result_file.write(moderation_output)
else:
    qa_data = pr_data["data"]

    prompt = "You are given a bunch of questions and answers pertaining to a document that contains interview transcripts for candidates that have been selected into companies, please flag the document into suitable for publishing on a public facing site or not. Provide a one liner reason flagging the parts that are problematic. We are defining problematic here as profanities/slurs etc. The text can be flagged if the content doesn't seem relevant to our interview experience publishing site too (basically we are trying to avoid spam and hateful speech). The text can be multilingual. You must output in this format: <Yes/No>. <Reasoning Highlighting the Problematic Parts if No>.\n\n"

    for question, answer in qa_data.items():
        if not len(answer): continue
        prompt += f"Question: {question}\nAnswer: {', '.join(answer)}\n\n"

print(prompt)