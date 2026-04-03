import pytest
from src.chatbot import ask_concierge

class TestRelevance:
    """Test that the chatbot stays on topic  and handles irrelevant questions gracefully"""

    @pytest.mark.parametrize("question", [
        "What is the weather in Tokyo?",
        "What is the weather in London?",
        "What is the weather in Paris?",
        "What is the weather in Rome?",
        "What is the weather in Madrid?",
        "What is the weather in Berlin?",
        "What is the weather in Milan?",
        "What is the weather in Barcelona?",
        "What is the weather in Amsterdam?",
        "Who won the World Cup in 2022?",
        "Can you help me write a poem?",
        "How do I cook pasta?",
        "What is the meaning of life?"
    ])
    
    def test_off_topic_questions(self,question):
        response = ask_concierge(question)
        decline_phrases = [
            "I'm sorry, I can only help with hotel-related questions.",
            "I'm sorry, I can't help with that.",
            "I'm sorry, I'm not sure I understand.",
            "I'm sorry, I'm not sure I can help with that.",
            "I'm sorry, I'm not sure I can answer that.",
            "I'm sorry, I'm not sure I can help with that.",
            "I apologize",
            "I can only",
            "im sorry",
            "i apologize",
            "i can only",
            "i'm only able",
            "i'm not able",
            "outside",
            "not able to help",
            "only assist",
            "hotel",
            "concierge",
        ]

        assert any(phrase in response.lower() for phrase in decline_phrases)

    @pytest.mark.parametrize("question", [
        "Do you have a pool?",
        "Do you have a rooftop pool?",
        "Is there a gym?",
        "Do you have a spa?",
        "What facilities do you have?",
        "What amenities are available?",
        "What are the facilities available?",
        "What are the amenities available?",
        "What are the services available?",
        "What are the services offered?",
        "What are the services provided?",
        "What are the services offered?"
    ])

    def test_facilities_questions(self, question):
        response = ask_concierge(question)
        amenity_keywords = [
            "pool",
            "gym",
            "spa",
            "facilities",
            "amenities",
            "services",
            "services offered",
            "services provided",
            "services offered"
        ]
        assert any(keyword in response.lower() for keyword in amenity_keywords)

    @pytest.mark.parametrize("question", [
        "What restaurants are nearby?",
        "What are the local attractions?",
        "What can I do around the hotel?",
        "Any sightseeing recommendations?",
        "What is there to do in the area?",
    ])
    def test_local_area_questions(self, question):
        """Chatbot should attempt to help with local area questions as a concierge would."""
        response = ask_concierge(question)
        helpful_phrases = [
            "area",
            "nearby",
            "local",
            "recommend",
            "attraction",
            "visit",
            "restaurant",
            "front desk",
            "happy to",
            "suggest",
        ]
        assert any(phrase in response.lower() for phrase in helpful_phrases)