def generate_response(emotion):
    responses = {
        "joy": "That's wonderful to hear! 😊",
        "sadness": "I'm here for you. It's okay to feel this way.",
        "anger": "I'm sorry that happened. Do you want to talk about it?",
        "fear": "You're not alone. I'm with you in this.",
        "love": "Aww, that's so heartwarming! 💖",
        "surprise": "Wow! That’s unexpected!",
        "neutral": "I understand. How can I help you today?"
    }
    return responses.get(emotion.lower(), "I'm here to listen, no matter what.")
