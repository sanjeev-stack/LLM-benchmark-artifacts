import json
import os
import csv

# Config
INPUT_FILE = "/Volumes/SecondaryStorage/BenchmarkingOfLLM/creative_writing_benchmark/creative_tasks.json"
RESPONSE_DIR = "responses"
OUTPUT_CSV = "creative_results.csv"
MODELS = ["llama3", "llama3.2"]

# Load prompts
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    prompts = {item["id"]: item for item in json.load(f)}

# Load model responses
model_outputs = {}
for model in MODELS:
    with open(os.path.join(RESPONSE_DIR, f"{model}.json"), "r", encoding="utf-8") as f:
        model_outputs[model] = {item["id"]: item["model_response"] for item in json.load(f)}

# Utility
def lexical_diversity(text):
    words = text.split()
    if not words:
        return 0
    unique_words = set(words)
    return round(len(unique_words) / len(words), 4)

# Output CSV
with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["id", "type"]
    for model in MODELS:
        fieldnames += [
            f"{model}_word_count",
            f"{model}_lexical_diversity"
        ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for task_id, task in prompts.items():
        row = {
            "id": task_id,
            "type": task["type"]
        }

        for model in MODELS:
            text = model_outputs[model].get(task_id, "")
            words = text.split()
            row[f"{model}_word_count"] = len(words)
            row[f"{model}_lexical_diversity"] = lexical_diversity(text)

        writer.writerow(row)

print(f"\nCreative evaluation complete. Results saved to: {OUTPUT_CSV}")