# Benchmarking Artifacts: LLaMA 3 vs. LLaMA 3.2

This repository contains the full benchmarking artifacts for evaluating LLaMA 3 and LLaMA 3.2 across three key tasks:

-  Question Answering
-  Text Summarization
-  Creative Writing

The artifacts include datasets, prompt templates, generated model responses, evaluation scripts, and final result metrics.

---

##  Directory Structure

creative_writing/
├── creative_results.csv
├── creative_tasks.json
├── evaluate_creative_response.py
├── run_creative_benchmark.py
└── responses/
    ├── llama3.json
    └── llama3.2.json

qa/
├── results.csv
├── qa_questions.json
├── evaluate_qa_response.py
├── run_qa_query.py
└── responses/
    ├── llama3.json
    └── llama3.2.json 

summarization/
├── summarization_results_with_bertscore.csv
├── summerization_tasks.json
├── evaluate_summerization_with_bertscore.py
├── run_summarization_benchmark.py
└── responses/
    ├── llama3.json
    └── llama3.2.json

---

##  How to Reproduce

Each folder contains:
- JSON prompt files
- Python scripts for inference (`run_*.py`)
- Scripts for metric evaluation (`evaluate_*.py`)
- Generated model responses and results

###  Requirements:
- Python 3.8+
- `pandas`, `json`, `os`

###  Example:
```bash
cd summarization/
python run_summarization_benchmark.py
python evaluate_summerization_with_bertscore.py



