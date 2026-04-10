# Hotel AI Chatbot QA Suite

A test suite for a hotel concierge chatbot powered by the Anthropic Claude API.
Covers correctness, relevance, tone, adversarial robustness, and RAG pipeline validation
across 100 test cases organised in a golden dataset.

---

[![Hotel AI Chatbot QA Suite](https://github.com/sharathsarangmath/hotel-ai-chatbot-test/actions/workflows/test.yml/badge.svg)](https://github.com/sharathsarangmath/hotel-ai-chatbot-test/actions/workflows/test.yml)

## Project Structure
```
hotel-ai-qa/
├── src/
│   ├── chatbot.py           # Hotel concierge chatbot (system under test)
│   ├── rag_chatbot.py       # RAG-powered chatbot using LlamaIndex
│   └── evaluator.py         # Custom LLM eval framework using Claude as judge
├── tests/
│   ├── test_correctness.py  # Factual accuracy tests
│   ├── test_relevance.py    # Topic relevance tests
│   ├── test_tone.py         # Tone and professionalism tests
│   ├── test_adversarial.py  # Adversarial red teaming tests
│   └── test_rag.py          # RAG pipeline tests
├── data/
│   ├── correctness_test_data.json
│   ├── relevance_test_data.json
│   ├── tone_test_data.json
│   ├── adversarial_test_data.json
│   └── rag_test_data.json
├── docs/
│   └── hotel_policy.txt     # Hotel knowledge base for RAG pipeline
├── .github/
│   └── workflows/
│       └── test.yml         # GitHub Actions CI pipeline
├── requirements.txt
└── pytest.ini
```

---

---

## Test Layers

### Layer 1 — Correctness (25 tests)
Validates that the chatbot answers factual questions accurately across multiple phrasings.
Test cases loaded from `data/correctness_test_data.json` covering check-in/out times, pet policy, parking, and breakfast hours.

### Layer 2 — Relevance (15 tests)
Validates that the chatbot stays on topic, handles off-topic questions appropriately,
and correctly answers questions about hotel facilities and local area.
Test cases loaded from `data/relevance_test_data.json`.

### Layer 3 — Tone (15 tests)
Validates that the chatbot always maintains a polite and professional tone,
even when guests are rude or abusive.
Test cases loaded from `data/tone_test_data.json`.

### Layer 4 — Adversarial Red Teaming (25 tests)
Validates that the chatbot resists:
- Prompt injection — attempts to override system instructions
- Jailbreaking — attempts to remove AI restrictions
- Hallucination traps — questions about non-existent hotel features
- Abuse — toxic responses to abusive messages
- Social engineering — fake authority claims

Test cases loaded from `data/adversarial_test_data.json`.

### Layer 5 — RAG Pipeline Testing (20 tests)
Validates the Retrieval Augmented Generation pipeline built with LlamaIndex.
Tests cover retrieval accuracy, semantic retrieval, hallucination resistance,
answer faithfulness, and no-context handling.
Test cases loaded from `data/rag_test_data.json`.

### Layer 6 — Chaos and Resilience Testing (15 tests)
Validates that both the standard chatbot and RAG chatbot handle failures gracefully.
Covers API timeouts, API errors, empty responses, malformed responses, empty input,
very long input, special characters, SQL injection attempts, and missing documents.
During chaos testing, 4 real bugs were found and fixed in error handling and
input validation across `src/chatbot.py` and `src/rag_chatbot.py`.

---

## Golden Dataset

Test cases are stored in separate JSON files under `data/` — one per test layer.
This separates test data from test logic, allowing non-technical stakeholders to
add or update test cases without touching Python code.
The golden dataset contains 100 test cases across 5 files.

| File | Tests | Description |
|---|---|---|
| `data/correctness_test_data.json` | 25 | Factual accuracy test cases |
| `data/relevance_test_data.json` | 15 | Topic relevance test cases |
| `data/tone_test_data.json` | 15 | Tone and professionalism test cases |
| `data/adversarial_test_data.json` | 25 | Adversarial red teaming test cases |
| `data/rag_test_data.json` | 20 | RAG pipeline test cases |
| **Total** | **100** | |

Chaos and resilience test cases are not stored in the golden dataset as they use
mock injection rather than real API calls — no input/output pairs to store.

---

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
python -m pytest tests/test_rag.py -v
```

---

| Tool | Purpose |
|---|---|
| Python 3.12 | Primary language |
| pytest | Test runner |
| pytest-html | Test reporting |
| Anthropic Claude API | Chatbot and LLM eval judge |
| LlamaIndex | RAG pipeline framework |
| HuggingFace Embeddings | Local text embeddings — no API cost |
| DeepEval | LLM eval framework (evaluated) |
| unittest.mock | Mock injection for chaos and resilience testing |
| GitHub Actions | CI/CD pipeline |

---

## Design Decisions

**Claude as eval judge:** Adversarial tests use Claude itself as the evaluation judge rather
than depending on OpenAI credentials. Scores responses for toxicity, faithfulness, and safety.

**Golden dataset:** Test cases live in separate JSON files under `data/`, one per layer.
Keeps test data separate from test logic. New cases can be added without touching Python.

**RAG pipeline:** Hotel knowledge is stored in a plain text file and indexed via LlamaIndex
with HuggingFace embeddings running locally. No external vector database required.

**Five-layer strategy:** Correctness, relevance, tone, adversarial robustness, and RAG validation.
