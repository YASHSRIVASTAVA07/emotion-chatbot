import joblib
from utils.preprocessor import clean_text
from utils.response_generator import generate_response

# Load model
model = joblib.load('models/emotion_model.pkl')

def chatbot_response(user_input):
    cleaned = clean_text(user_input)
    emotion = model.predict([cleaned])[0]
    reply = generate_response(emotion)
    return reply, emotion
