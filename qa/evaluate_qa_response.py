import json
import os
import csv

# Input
RESPONSE_DIR = "responses"
QUESTIONS_FILE = "/Volumes/SecondaryStorage/BenchmarkingOfLLM/BenchmarkQA/qa_questions.json"
MODELS = ["llama3", "llama3.2"]
OUTPUT_CSV = "results.csv"

# Load original questions + answers
with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions = {q["id"]: q for q in json.load(f)}

# Load responses from each model
model_outputs = {}
for model in MODELS:
    with open(os.path.join(RESPONSE_DIR, f"{model}.json"), "r", encoding="utf-8") as f:
        model_outputs[model] = {item["id"]: item["model_response"] for item in json.load(f)}

# Utility: normalize for comparison
def normalize(text):
    return text.lower().strip().replace(",", "").replace(".", "")

# Compare responses and write CSV
with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["id", "question", "expected_answer"] + \
                 [f"{model}_response" for model in MODELS] + \
                 [f"{model}_match" for model in MODELS]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for qid, q in questions.items():
        row = {
            "id": qid,
            "question": q["question"],
            "expected_answer": q["answer"]
        }

        expected_norm = normalize(q["answer"])

        for model in MODELS:
            response = model_outputs[model].get(qid, "")
            response_norm = normalize(response)
            row[f"{model}_response"] = response
            row[f"{model}_match"] = "matched" if expected_norm in response_norm else "not matched"

        writer.writerow(row)

print(f"\n🎯 Evaluation complete! Results saved to: {OUTPUT_CSV}")