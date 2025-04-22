import json
import os
import csv
from bert_score import score

# Config
INPUT_FILE = "/Volumes/SecondaryStorage/BenchmarkingOfLLM/summarization_benchmark/summerization_tasks.json"
RESPONSE_DIR = "responses"
OUTPUT_CSV = "summarization_results_with_bertscore.csv"
MODELS = ["llama3", "llama3.2"]

# Load reference summaries
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    tasks = {item["id"]: item for item in json.load(f)}

# Load model summaries
model_summaries = {}
for model in MODELS:
    file_path = os.path.join(RESPONSE_DIR, f"{model}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        model_summaries[model] = {item["id"]: item["model_summary"] for item in json.load(f)}

# Prepare output CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["id", "type"]

    for model in MODELS:
        fieldnames += [
            f"{model}_bertscore_precision",
            f"{model}_bertscore_recall",
            f"{model}_bertscore_f1"
        ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for task_id, task in tasks.items():
        row = {
            "id": task_id,
            "type": task["type"]
        }

        ref = [task["reference_summary"]]

        for model in MODELS:
            hyp = [model_summaries[model].get(task_id, "")]
            P, R, F1 = score(hyp, ref, lang="en", verbose=False)

            row[f"{model}_bertscore_precision"] = round(P.item(), 4)
            row[f"{model}_bertscore_recall"] = round(R.item(), 4)
            row[f"{model}_bertscore_f1"] = round(F1.item(), 4)

        writer.writerow(row)

print(f"\n BERTScore evaluation complete! Saved to: {OUTPUT_CSV}")