import json
import os
import requests
from time import sleep

# Configuration
INPUT_FILE = "/Volumes/SecondaryStorage/BenchmarkingOfLLM/summarization_benchmark/summerization_tasks.json"
RESPONSE_DIR = "responses"
WAIT_BETWEEN_REQUESTS = 1  # seconds
OLLAMA_URL = "http://localhost:11434/api/generate"

# Models to benchmark
MODELS = {
    "llama3": "llama3",
    "llama3.2": "llama3:latest"
}

# Ensure output directory exists
os.makedirs(RESPONSE_DIR, exist_ok=True)

# Load summarization tasks
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    tasks = json.load(f)

# Function to query Ollama
def query_model(model: str, source_text: str) -> str:
    prompt = f"Summarize the following text:\n\n{source_text}"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Error querying {model}: {e}")
        return "ERROR"

# Run benchmark
for key, model_name in MODELS.items():
    print(f"\nRunning summarization for {key}")
    results = []

    for task in tasks:
        print(f"- Summarizing task {task['id']}")
        summary = query_model(model_name, task["source"])

        results.append({
            "id": task["id"],
            "type": task["type"],
            "source": task["source"],
            "reference_summary": task["reference_summary"],
            "model_summary": summary
        })

        sleep(WAIT_BETWEEN_REQUESTS)

    output_path = os.path.join(RESPONSE_DIR, f"{key}.json")
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(results, f_out, indent=2)

    print(f"Saved results to: {output_path}")