import pytest
from src.chatbot import ask_concierge

class TestCorrectness:

    """Test the correctness of the chatbot"""

    @pytest.mark.parametrize("question", [
        "What time is check-in?",
        "When can i check-in?",
        "What are the checkin times?",
        "Checkin time?",
        "what's the earlest i can get my room?"
    ])

    def test_checkin_time(self, question):
        response = ask_concierge(question)
        assert "3" in response and ("pm" in response.lower() or "PM" in response)

    @pytest.mark.parametrize("question", [
        "What time is check-out?",
        "When can i check-out?",
        "What are the checkout times?",
        "Checkout time?",
        "When should i vacate my room?",
        "When do i need to leave?"
    ])

    def test_checkout_time(self, question):
        response = ask_concierge(question)
        assert "11" in response and ("am" in response.lower() or "AM" in response)

    @pytest.mark.parametrize("question", [
        "Are pets allowed?",
        "Do you allow pets?",
        "Can i bring my dog?",
        "Are pets allowed in the hotel?",
        "Do you have a pet policy?",
        "Can i bring my cat?"
    ])
    def test_pet_policy(self, question):
        response = ask_concierge(question)
        assert "not allowed" in response.lower() or "no pets" in response.lower() or "pets not allowed" in response.lower()

    @pytest.mark.parametrize("question", [
        "Do you have parking?",
        "Is parking available?",
        "Do you offer parking for guests?",
        "Is parking free?",
        "Where can i park?"
    ])
    def test_parking(self, question):
        response = ask_concierge("Do you have parking?")
        assert "free" in response.lower() or "parking available" in response.lower() or "parking available at site" in response.lower()
    
    @pytest.mark.parametrize("question", [
        "What time is breakfast?",
        "When is breakfast served?",
        "What are the breakfast times?",
        "Breakfast time?",
        "When can i have breakfast?",
        "What time do you serve breakfast?"
    ])
    def test_breakfast_time(self, question):
        response = ask_concierge(question)
        assert "7" in response and ("am" in response.lower() or "AM" in response)
    