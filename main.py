import streamlit as st
import langchain_yt_bot as lch



# Set page configuration
st.set_page_config(
    page_title="Youtube Video Assistant",
    page_icon="📽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .user-bubble {
        background-color: #ff6b6b;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        display: inline-block;
        max-width: 80%;
    }
    .bot-bubble {
        background-color: #f9a825;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        display: inline-block;
        max-width: 80%;
    }
    .avatar {
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        margin-right: 10px;
    }
    .message-container {
        display: flex;
        align-items: flex-start;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for YouTube URL and chat history
if "youtube_url" not in st.session_state:
    st.session_state.youtube_url = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Input YouTube URL Section ---
if not st.session_state.youtube_url:
    st.title("Enter YouTube Video URL")
    youtube_url_input = st.text_input("YouTube URL:")
    if st.button("Proceed to Chat"):
        if youtube_url_input:
            st.session_state.youtube_url = youtube_url_input
            st.rerun()
        else:
            st.warning("Please enter a YouTube URL.")
else:
    # --- Chat Interface ---
    st.title("YouTube Video Assistant")
    st.subheader(f"Chatting about: {st.session_state.youtube_url}")

    # Function to add messages to chat history and display them
    def add_message(role, content):
        st.session_state.chat_history.append({"role": role, "content": content})

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.container():
                col1, col2 = st.columns([1, 9])
                with col1:
                    st.markdown(f"""
                    <div class="avatar" style="background-color: #ff6b6b;">
                        👤
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="user-bubble">
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            with st.container():
                col1, col2 = st.columns([1, 9])
                with col1:
                    st.markdown(f"""
                    <div class="avatar" style="background-color: #f9a825;">
                        🤖
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="bot-bubble">
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

    # User input area at the bottom of the page
    with st.container():
        # Create a form to prevent rerun on each keystroke
        with st.form(key="message_form", clear_on_submit=True):
            col1, col2 = st.columns([8, 1])
            with col1:
                user_input = st.text_input("", placeholder="Send a message...", label_visibility="collapsed")
            with col2:
                submit_button = st.form_submit_button("Send")

            if submit_button and user_input:
                # Add user message to chat
                add_message("user", user_input)

                # Get response from the chat function, passing the youtube_url
                response = lch.generate_answer_from_query(query=user_input,youtube_url=st.session_state.youtube_url)

                # Add bot response to chat
                add_message("bot", response)      # Rerun to update the displayed chat
                st.rerun()