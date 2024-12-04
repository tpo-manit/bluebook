import json
import ollama

with open('/tmp/qa_data.json', 'r') as infile:
    data = json.load(infile)

qa_data = data['pr_data']['data']

prompt = "You are given a bunch of questions and answers pertaining to a document that contains interview transcripts for candidates that have been selected into companies, please flag the document into suitable for publishing on a public facing site or not. Provide a one liner reason flagging the parts that are problematic. We are defining problematic here as profanities/slurs etc. The text can be flagged if the content doesn't seem relevant to our interview experience publishing site too (basically we are trying to avoid spam and hateful speech). The text can be multilingual. You must output in this format: <Yes/No>. <Reasoning Highlighting the Problematic Parts>.\n\n"

for question, answer in qa_data.items():
    prompt += f"Question: {question}\nAnswer: {', '.join(answer)}\n\n"

response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

moderation_output = response['text']

with open('/tmp/moderation_result.txt', 'w') as result_file:
    result_file.write(moderation_output)

print(moderation_output)