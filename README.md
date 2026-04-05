# Hotel AI Chatbot QA Suite

A comprehensive AI/LLM test suite for a hotel concierge chatbot built on the Anthropic Claude API.
This project demonstrates production-grade QA engineering practices for AI agent testing including
correctness evaluation, relevance testing, tone validation, and adversarial red teaming.

---

## Project Structure
```
hotel-ai-qa/
├── src/
│   ├── chatbot.py           # Hotel concierge chatbot (system under test)
│   └── evaluator.py         # Custom LLM eval framework using Claude as judge
├── tests/
│   ├── test_correctness.py  # Factual accuracy tests
│   ├── test_relevance.py    # Topic relevance tests
│   ├── test_tone.py         # Tone and professionalism tests
│   └── test_adversarial.py  # Adversarial red teaming tests
├── .github/
│   └── workflows/
│       └── test.yml         # GitHub Actions CI pipeline
├── requirements.txt
└── pytest.ini
```

---

## Test Layers

### Layer 1 — Correctness (25 tests)
Validates that the chatbot answers factual questions accurately across multiple phrasings.
Test cases loaded from `data/correctness_cases.json` covering check-in/out times, pet policy, parking costs, and breakfast hours.

### Layer 2 — Relevance (15 tests)
Validates that the chatbot stays on topic, handles off-topic questions appropriately,
and correctly answers questions about hotel facilities and local area.
Test cases loaded from `data/relevance_cases.json`.

### Layer 3 — Tone (15 tests)
Validates that the chatbot always maintains a polite and professional tone —
even when guests are rude or abusive.
Test cases loaded from `data/tone_cases.json`.

### Layer 4 — Adversarial Red Teaming (25 tests)
Validates that the chatbot resists prompt injection, jailbreaking, hallucination traps,
abuse, and social engineering attempts.
Test cases loaded from `data/adversarial_cases.json`.

---

## Golden Dataset

Test cases are stored in separate JSON files under `data/` — one per test layer.
This separates test data from test logic, allowing non-technical stakeholders to
add or update test cases without touching Python code.

| File | Tests | Description |
|---|---|---|
| `data/correctness_cases.json` | 25 | Factual accuracy test cases |
| `data/relevance_cases.json` | 15 | Topic relevance test cases |
| `data/tone_cases.json` | 15 | Tone and professionalism test cases |
| `data/adversarial_cases.json` | 25 | Adversarial red teaming test cases |


## Custom LLM Eval Framework

Instead of keyword matching alone, adversarial tests use a custom eval framework
that uses Claude as a judge to score responses on three dimensions:

| Metric | Description | Pass Threshold |
|---|---|---|
| `evaluate_toxicity` | Scores response for harmful or inappropriate content | < 0.3 |
| `evaluate_faithfulness` | Scores response for factual grounding | > 0.7 |
| `evaluate_safety` | Scores response for resistance to manipulation | > 0.7 |

---

## Running the Tests

### Install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set up environment
```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run a specific layer
```bash
python -m pytest tests/test_correctness.py -v
python -m pytest tests/test_relevance.py -v
python -m pytest tests/test_tone.py -v
python -m pytest tests/test_adversarial.py -v
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Primary language |
| pytest | Test runner |
| pytest-html | Test reporting |
| Anthropic Claude API | Chatbot and LLM eval judge |
| DeepEval | LLM eval framework (evaluated) |
| GitHub Actions | CI/CD pipeline |

---

## Key Design Decisions

**Claude as eval judge:** Rather than using OpenAI-dependent frameworks, this project uses
Claude itself as the evaluation judge — scoring responses for toxicity, faithfulness, and safety.
This keeps the stack consistent and demonstrates understanding of LLM-as-judge evaluation patterns.

**Parametrized test cases:** Each test covers multiple phrasings of the same question,
reflecting how real users interact with conversational AI in unpredictable ways.

**Four-layer test strategy:** Mirrors production AI QA practices — functional correctness,
scope relevance, tone safety, and adversarial robustness.