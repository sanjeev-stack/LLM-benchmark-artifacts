print("Hi")
import json
import os
import requests
from time import sleep

# Config
MODEL_VERSIONS = {
    "llama3": "llama3",
    "llama3.2": "llama3:latest"
}
INPUT_FILE = "/Volumes/SecondaryStorage/BenchmarkingOfLLM/BenchmarkQA/qa_questions.json"
RESPONSE_DIR = "responses"
WAIT_BETWEEN_REQUESTS = 1  # seconds
OLLAMA_URL = "http://localhost:11434/api/generate"

# Ensure output directory exists
os.makedirs(RESPONSE_DIR, exist_ok=True)

# Load questions
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

# Function to query Ollama HTTP API
def query_ollama_http(model: str, prompt: str) -> str:
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
        print(f"Request failed: {e}")
        return "ERROR"

# Run benchmark
for model_key, model_name in MODEL_VERSIONS.items():
    print(f"\n=== Running QA benchmark for {model_key} ===")
    model_results = []

    for item in questions:
        print(f"Q: {item['question']}")
        response = query_ollama_http(model_name, item["question"])
        print(f"A: {response}\n")

        model_results.append({
            "id": item["id"],
            "question": item["question"],
            "expected_answer": item["answer"],
            "model_response": response
        })

        sleep(WAIT_BETWEEN_REQUESTS)

    # Save responses
    output_file = os.path.join(RESPONSE_DIR, f"{model_key}.json")
    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(model_results, f_out, indent=2)

    print(f"Saved results to {output_file}")