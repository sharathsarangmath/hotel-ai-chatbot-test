import pytest
from src.chatbot import ask_concierge
from src.rag_chatbot import ask_rag_concierge, build_rag_engine
from unittest.mock import patch, MagicMock

class TestChaos:
    
    def test_api_timeout(self):
        with patch("anthropic.Anthropic.messages") as mock:
            mock.create.side_effects = TimeoutError("API timed out")
            try:
                response = ask_concierge("What time is the checkin?")
                assert response is not None
            except TimeoutError:
                pytest.fail("Chatbot did not handle time out gracefully")

    
    def test_api_error(self):
        """Chatbot should handle API errors gracefully."""
        with patch("anthropic.Anthropic.messages") as mock:
            mock.create.side_effect = Exception("Internal server error")
            try:
                response = ask_concierge("What time is check-in?")
                assert response is not None
            except Exception:
                pytest.fail("Chatbot did not handle API error gracefully")

    def test_empty_response(self):
        """Chatbot should handle empty API response gracefully."""
        with patch("anthropic.Anthropic.messages") as mock:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text="")]
            mock.create.return_value = mock_response
            response = ask_concierge("What time is check-in?")
            assert response is not None
            assert isinstance(response, str)

    def test_malformed_response(self):
        """Chatbot should handle malformed API response gracefully."""
        with patch("anthropic.Anthropic.messages") as mock:
            mock_response = MagicMock()
            mock_response.content = []
            mock.create.return_value = mock_response
            try:
                response = ask_concierge("What time is check-in?")
                assert response is not None
            except Exception:
                pytest.fail("Chatbot did not handle malformed response gracefully")

    def test_empty_input(self):
        """Chatbot should handle empty input gracefully."""
        response = ask_concierge("")
        assert response is not None
        assert isinstance(response, str)

    def test_very_long_input(self):
        """Chatbot should handle very long inputs without crashing."""
        long_input = "What time is check-in? " * 100
        try:
            response = ask_concierge(long_input)
            assert response is not None
        except Exception:
            pytest.fail("Chatbot crashed on very long input")

    def test_special_characters(self):
        """Chatbot should handle special characters in input."""
        response = ask_concierge("What time is check-in??? 🏨 #hotel @marriott")
        assert response is not None
        assert isinstance(response, str)

    def test_sql_injection_attempt(self):
        """Chatbot should handle SQL injection attempts gracefully."""
        response = ask_concierge("'; DROP TABLE hotels; --")
        assert response is not None
        assert isinstance(response, str)


class TestChaosRAG:
    """Chaos and resilience tests for the RAG chatbot."""

    @pytest.fixture(scope="class")
    def rag_engine(self):
        """Build RAG engine once for the entire class."""
        return build_rag_engine()

    def test_rag_empty_input(self, rag_engine):
        """RAG chatbot should handle empty input gracefully."""
        response = ask_rag_concierge("", rag_engine)
        assert response is not None
        assert isinstance(response, str)

    def test_rag_very_long_input(self, rag_engine):
        """RAG chatbot should handle very long inputs without crashing."""
        long_input = "What time is check-in? " * 100
        try:
            response = ask_rag_concierge(long_input, rag_engine)
            assert response is not None
        except Exception:
            pytest.fail("RAG chatbot crashed on very long input")

    def test_rag_special_characters(self, rag_engine):
        """RAG chatbot should handle special characters in input."""
        response = ask_rag_concierge("What time is check-in??? 🏨 #hotel @marriott", rag_engine)
        assert response is not None
        assert isinstance(response, str)

    def test_rag_sql_injection_attempt(self, rag_engine):
        """RAG chatbot should handle SQL injection attempts gracefully."""
        response = ask_rag_concierge("'; DROP TABLE hotels; --", rag_engine)
        assert response is not None
        assert isinstance(response, str)

    def test_rag_missing_docs(self):
        """RAG pipeline should handle missing documents gracefully."""
        with patch("llama_index.core.SimpleDirectoryReader") as mock:
            mock.return_value.load_data.return_value = []
            try:
                engine = build_rag_engine()
                assert engine is not None
            except Exception:
                pytest.fail("RAG pipeline did not handle missing docs gracefully")

    def test_rag_api_timeout(self, rag_engine):
        """RAG chatbot should handle API timeout gracefully."""
        with patch("llama_index.llms.anthropic.Anthropic.complete") as mock:
            mock.side_effect = TimeoutError("API timed out")
            try:
                response = ask_rag_concierge("What time is check-in?", rag_engine)
                assert response is not None
            except TimeoutError:
                pytest.fail("RAG chatbot did not handle timeout gracefully")

    def test_rag_api_error(self, rag_engine):
        """RAG chatbot should handle API errors gracefully."""
        with patch("llama_index.llms.anthropic.Anthropic.complete") as mock:
            mock.side_effect = Exception("Internal server error")
            try:
                response = ask_rag_concierge("What time is check-in?", rag_engine)
                assert response is not None
            except Exception:
                pytest.fail("RAG chatbot did not handle API error gracefully")