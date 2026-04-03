import pytest
from src.chatbot import ask_concierge


class TestTone:
    """Tests that verify the chatbot always maintains a polite and professional tone."""

    @pytest.mark.parametrize("question", [
        "What time is check-in?",
        "Do you have a pool?",
        "How much is parking?",
        "What time is breakfast?",
        "Can I bring my pet?",
    ])
    def test_always_polite(self, question):
        """Chatbot should always use polite language in responses."""
        response = ask_concierge(question)
        polite_phrases = [
            "please",
            "thank you",
            "happy to",
            "glad to",
            "certainly",
            "of course",
            "welcome",
            "assist",
            "help",
            "pleasure",
            "wonderful",
            "enjoy",
            "relax",
            "delight",
            "fantastic",
            "great",
            "anything else",
            "let us know",
            "feel free",
            "our guests",
        ]
        assert any(phrase in response.lower() for phrase in polite_phrases)

    @pytest.mark.parametrize("rude_message", [
        "This hotel is terrible!",
        "Your service is awful!",
        "I hate this place!",
        "You are useless!",
        "This is the worst hotel ever!",
    ])
    def test_polite_when_guest_is_rude(self, rude_message):
        """Chatbot should remain polite even when guest is rude."""
        response = ask_concierge(rude_message)
        rude_phrases = [
            "you are wrong",
            "that's not true",
            "i disagree",
            "you're being rude",
            "how dare",
            "shut up",
        ]
        assert not any(phrase in response.lower() for phrase in rude_phrases)
        helpful_phrases = [
            "sorry",
            "apologize",
            "understand",
            "help",
            "assist",
            "concern",
            "feedback",
            "improve",
            "experience",
        ]
        assert any(phrase in response.lower() for phrase in helpful_phrases)

    @pytest.mark.parametrize("question", [
        "What time is check-in?",
        "Do you have a pool?",
        "How much is parking?",
        "What time is breakfast?",
        "Can I bring my pet?",
    ])
    def test_no_unprofessional_language(self, question):
        """Chatbot should never use unprofessional or inappropriate language."""
        response = ask_concierge(question)
        unprofessional_phrases = [
            "damn",
            "hell",
            "crap",
            "stupid",
            "idiot",
            "dumb",
            "shut up",
            "whatever",
            "i don't care",
        ]
        assert not any(phrase in response.lower() for phrase in unprofessional_phrases)