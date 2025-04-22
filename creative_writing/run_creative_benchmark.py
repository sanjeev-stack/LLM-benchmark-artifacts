import json
import os
import requests
from time import sleep

# Configuration
INPUT_FILE = "/Volumes/SecondaryStorage/BenchmarkingOfLLM/creative_writing_benchmark/creative_tasks.json"
RESPONSE_DIR = "responses"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELS = {
    "llama3": "llama3",
    "llama3.2": "llama3:latest"
}
WAIT_BETWEEN_REQUESTS = 1  # seconds

# Ensure output folder exists
os.makedirs(RESPONSE_DIR, exist_ok=True)

# Load prompts
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)

# Function to call Ollama API
def generate_response(model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except Exception as e:
        print(f"[ERROR] Failed on model {model}: {e}")
        return "ERROR"

# Run benchmark
for key, model_name in MODELS.items():
    print(f"\nGenerating creative outputs using {key}...")
    results = []

    for task in prompts:
        print(f"- Prompt {task['id']}: {task['type']}")
        output = generate_response(model_name, task["prompt"])

        results.append({
            "id": task["id"],
            "type": task["type"],
            "prompt": task["prompt"],
            "model_response": output
        })

        sleep(WAIT_BETWEEN_REQUESTS)

    # Save model output
    out_file = os.path.join(RESPONSE_DIR, f"{key}.json")
    with open(out_file, "w", encoding="utf-8") as f_out:
        json.dump(results, f_out, indent=2)

    print(f"Responses saved to: {out_file}")