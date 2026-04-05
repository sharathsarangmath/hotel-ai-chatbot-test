import json
import pytest
from src.chatbot import ask_concierge
from src.evaluater import evaluate_toxicity, evaluate_faithfulness, evaluate_safety

HOTEL_CONTEXT = """
Check-in time is 3:00 PM. Check-out time is 11:00 AM.
The hotel has a rooftop pool, a gym, and a spa.
The restaurant serves breakfast from 7:00 AM to 11:00 AM.
Pets are not allowed.
Parking is available for free.
"""


def load_cases(category=None):
    """Load test cases from golden dataset."""
    with open("data/adversarial_test_data.json") as f:
        cases = json.load(f)
    if category:
        cases = [c for c in cases if c["category"] == category]
    return cases


class TestAdversarial:
    """Tests that verify the chatbot handles adversarial inputs safely."""

    @pytest.mark.parametrize("case", load_cases())
    def test_adversarial(self, case):
        """Chatbot should handle adversarial inputs safely."""
        response = ask_concierge(case["input"])

        if case["eval_type"] == "safety":
            score = evaluate_safety(response)
            assert score >= case["threshold"], (
                f"Test ID: {case['id']}\n"
                f"Category: {case['category']}\n"
                f"Input: {case['input']}\n"
                f"Safety score too low: {score:.2f} (threshold: {case['threshold']})\n"
                f"Got: {response}"
            )

        elif case["eval_type"] == "faithfulness":
            score = evaluate_faithfulness(response, HOTEL_CONTEXT)
            assert score >= case["threshold"], (
                f"Test ID: {case['id']}\n"
                f"Category: {case['category']}\n"
                f"Input: {case['input']}\n"
                f"Faithfulness score too low: {score:.2f} (threshold: {case['threshold']})\n"
                f"Got: {response}"
            )

        elif case["eval_type"] == "toxicity":
            score = evaluate_toxicity(response)
            assert score < case["threshold"], (
                f"Test ID: {case['id']}\n"
                f"Category: {case['category']}\n"
                f"Input: {case['input']}\n"
                f"Toxicity score too high: {score:.2f} (threshold: {case['threshold']})\n"
                f"Got: {response}"
            )