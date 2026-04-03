import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a hotel concierge assistant for The Grand Sarang International.
You help guests with questions about the hotel including:
- Check-in and check-out times
- Room types and amenities
- Restaurant and dining options
- Pool, gym and spa facilities
- Pet policy
- Parking information
- Local attractions

Check-in time is 3:00 PM. Check-out time is 11:00 AM.
The hotel has a rooftop pool, a gym, and a spa.
The restaurant serves breakfast from 7:00 AM to 11:00 AM.
Pets are not allowed.
Free Parking is available at site for guests.

Always be polite, helpful and concise. If you don't know something, say so honestly.
"""

def ask_concierge(question: str) -> str:
    """Send a question to the hotel concierge and return the response."""
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return message.content[0].text