import sys
import os

# Add the parent directory to sys.path (keeping the original system path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

# Import the chatbot module
from app.chatbot import chatbot_response
import streamlit as st
import time
from collections import Counter
import altair as alt
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Emotion Chatbot",
    page_icon="🤖",
    layout="centered",
)

# Apply custom CSS for better styling
st.markdown("""
<style>
    /* Set all text to black */
    .chat-message {
    color: #000000 !important;
}

.emotion-chart, .emotion-meter, .meter-label {
    color: white !important;
}
    
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.8rem; 
        margin-bottom: 1rem; 
        display: flex;
        align-items: flex-start;
        color: #000000;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 5px solid #1976D2;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .chat-message.bot {
        background-color: #f5f5f5;
        border-left: 5px solid #388E3C;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .emotion-tag {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 2rem;
        font-size: 0.85rem;
        margin-top: 0.7rem;
        color: white !important; /* Keep tag text white for contrast */
        font-weight: bold;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .st-emotion-cache-13ln4jg {
        padding-top: 2rem;
    }
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        padding: 0;
        color: white !important; /* Keep title text white for contrast */
    }
    .title-emoji {
        font-size: 3rem;
        margin-right: 0.5rem;
    }
    .typing-indicator {
        display: inline-flex;
        align-items: center;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background-color: #888;
        border-radius: 50%;
        display: inline-block;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1.0); }
    }
    .stTextInput > div > div > input {
        border-radius: 2rem;
        padding-left: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    .stButton > button {
        border-radius: 2rem;
        font-weight: bold;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .analytics-button {
        background-color: #673AB7;
        color: white !important;
    }
    .analytics-button:hover {
        background-color: #5E35B1;
    }
    .clear-button {
        background-color: #f44336;
        color: white !important;
    }
    .clear-button:hover {
        background-color: #d32f2f;
    }
    .emotion-chart {
        border-radius: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        padding: 1rem;
        background-color: white;
    }
    .emotion-meter {
        margin-top: 1rem;
        padding: 1rem;
        background-color: white;
        border-radius: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .meter-container {
        margin-bottom: 0.8rem;
    }
    .meter-label {
        margin-bottom: 0.3rem;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        color: white;
    }
    .meter-bar {
        height: 0.8rem;
        border-radius: 0.4rem;
        background-color: #e0e0e0;
    }
    .meter-fill {
        height: 100%;
        border-radius: 0.4rem;
    }
    /* Force black text in the bottom hint */
    .footer-hint {
        color: white !important;
    }
    /* Make form button text white for contrast */
    .stButton>button {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to get emotion color based on detected emotion
def get_emotion_color(emotion):
    emotion_colors = {
        "happy": "#FFC107",      # Amber
        "sad": "#2196F3",        # Blue
        "angry": "#F44336",      # Red
        "surprised": "#9C27B0",  # Purple
        "fearful": "#FF5722",    # Deep Orange
        "disgusted": "#4CAF50",  # Green
        "neutral": "#607D8B",    # Blue Grey
    }
    return emotion_colors.get(emotion.lower(), "#607D8B")

# Function to get emoji for emotion
def get_emotion_emoji(emotion):
    emotion_emojis = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😠",
        "surprised": "😲",
        "fearful": "😨",
        "disgusted": "🤢",
        "neutral": "😐",
    }
    return emotion_emojis.get(emotion.lower(), "😐")

# Custom header with emoji
st.markdown(
    """
    <div class="title-container">
        <span class="title-emoji">🤖</span>
        <h1 class="title-text">Emotion Chatbot</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize show_analytics in session state if it doesn't exist
if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False

# Function to toggle analytics visibility
def toggle_analytics():
    st.session_state.show_analytics = not st.session_state.show_analytics

# Function to clear chat
def clear_chat():
    st.session_state.chat_history = []

# Create two columns for buttons
col1, col2 = st.columns(2)

# Add the analytics and clear buttons
with col1:
    st.button("Show Emotion Analytics", on_click=toggle_analytics, key="analytics_button", 
              use_container_width=True, type="primary")
with col2:
    st.button("Clear Chat", on_click=clear_chat, key="clear_button", 
              use_container_width=True)

# Show emotion analytics if toggled
if st.session_state.show_analytics and st.session_state.chat_history:
    # Extract emotions from chat history
    emotions = [msg["emotion"] for msg in st.session_state.chat_history if msg.get("role") == "assistant" and "emotion" in msg]
    
    if emotions:
        # Count emotions
        emotion_counts = Counter(emotions)
        total = sum(emotion_counts.values())
        
        st.markdown("### Emotion Analysis")
        
        # Create data for chart
        chart_data = pd.DataFrame({
            'Emotion': list(emotion_counts.keys()),
            'Count': list(emotion_counts.values())
        })
        
        # Create chart
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Emotion:N', sort='-y', title=None),
            y=alt.Y('Count:Q', title=None),
            color=alt.Color('Emotion:N', scale=alt.Scale(
                domain=list(emotion_counts.keys()),
                range=[get_emotion_color(e) for e in emotion_counts.keys()]
            ), legend=None),
            tooltip=['Emotion', 'Count']
        ).properties(
            height=200
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14,
            labelColor='black',
            titleColor='black'
        )
        
        # Display chart
        st.altair_chart(chart, use_container_width=True)
        
        # Create emotion meters
        st.markdown("### Emotion Meter")
        for emotion, count in emotion_counts.items():
            percentage = (count / total) * 100
            color = get_emotion_color(emotion)
            emoji = get_emotion_emoji(emotion)
            
            st.markdown(f"""
            <div class="meter-container">
                <div class="meter-label">
                    <span>{emotion.capitalize()} {emoji}</span>
                    <span>{percentage:.1f}%</span>
                </div>
                <div class="meter-bar">
                    <div class="meter-fill" style="width: {percentage}%; background-color: {color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Display chat messages from history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div>
                <b>You:</b><br>{message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        emotion = message["emotion"]
        emotion_color = get_emotion_color(emotion)
        emotion_emoji = get_emotion_emoji(emotion)
        st.markdown(f"""
        <div class="chat-message bot">
            <div>
                <b>Bot:</b><br>{message["content"]}
                <div><span class="emotion-tag" style="background-color: {emotion_color};">
                    {emotion_emoji}
                </span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Container for the typing indicator
typing_container = st.empty()

# Create a form for input to prevent rerun issues
with st.form(key="message_form", clear_on_submit=True):
    user_message = st.text_input(
        "Message",  # Label for accessibility
        value="",
        placeholder="Type your message here...",
        label_visibility="collapsed"  # Hide label but keep it for accessibility
    )
    submit_button = st.form_submit_button("Send")

# Handle form submission
if submit_button and user_message:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # Display typing indicator while processing
    typing_container.markdown("""
    <div class="chat-message bot">
        <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get bot response
    reply, emotion = chatbot_response(user_message)
    
    # Simulate a short delay to show the typing indicator
    time.sleep(0.5)
    
    # Clear typing indicator
    typing_container.empty()
    
    # Add bot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": reply, "emotion": emotion})
    
    # Rerun the app to display the updated chat history
    st.rerun()

# Display a hint about the chatbot's capabilities at the bottom
st.markdown("---")
st.markdown("""
    <small class="footer-hint" style="color:white; font-size: 14px; text-align: center;">This chatbot can detect emotions like happy, sad, angry, surprised, fearful, disgusted, and neutral. Try expressing different emotions to see how the bot responds!</small>
""", unsafe_allow_html=True)