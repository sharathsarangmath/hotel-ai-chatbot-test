import json
import pytest
from src.rag_chatbot import ask_rag_concierge, build_rag_engine

def load_cases(category=None):
    with open("data/rag_test_data.json") as f:
        cases = json.load(f)
    if category:
        cases = [c for c in cases if f["category"]==category]
    return cases

@pytest.fixture(scope="session")

def rag_engine():
    return build_rag_engine()

class TestRag:
    @pytest.mark.parametrize("case",load_cases())

    def test_rag(self, case, rag_engine):
        response = ask_rag_concierge(case["input"],rag_engine)
        assert any(
            keyword.lower() in response.lower()
            for keyword in case["expected_keywords"]
        ),(
            f"Text ID: {case['id']}\n",
            f"Category: {case['category']}\n",
            f"Input: {case['input']}\n",
            f"Expected one of: {case['expected_keywords']}\n",
            f"Got: {response}"
        )