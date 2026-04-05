import pytest
from src.chatbot import ask_concierge
import json

def load_cases(category=None):
    with open("data/relevance_test_data.json") as f:
        cases = json.load(f)
    if category:
        cases = [c for c in cases if c["category"]==category]
    return cases

class TestRelevance:
    """Test that the chatbot stays on topic  and handles irrelevant questions gracefully"""

    @pytest.mark.parametrize("case",load_cases())
    
    def test_relevance(self,case):
        response = ask_concierge(case["input"])
        assert any(
            keyword in response.lower()
            for keyword in case["expected_keywords"]
        ),(
            f"Test ID: {case['id']}\n"
            f"Category: {case['category']}\n"
            f"Input: {case['input']}\n"
            f"Expected one of: {case['expected_keywords']}\n"
            f"Got: {response}"
        )
        