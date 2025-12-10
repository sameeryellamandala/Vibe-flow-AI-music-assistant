import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

st.set_page_config( page_title = "VIBE-FLOW", page_icon= "🎧")

st.title("🎧 VibeFlow - AI Music Assistant")
st.subheader("Your smart music companion. Select language & mood to get perfect playlists.")


api_key = st.sidebar.text_input(label = "enter valid groq-api-key",value = "",type="password")

if not api_key.strip():
    st.write("please enter groq api_key first:")
    st.stop() 


try:
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=api_key
    )
    llm.invoke("ping")   # test call
except Exception as e:
    st.error("❌ Invalid API Key. Please provide a valid NVIDIA API key.")
    st.stop()

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are VibeFlow — an AI music expert. "
     "Your job is to provide a curated list of the top 10 - 15 most popular songs  sung by the singer  based on the user's "
     "selected language, music type and singer "
     "For each song, include:\n"
     "1. Song Name\n"
     "2. YouTube search link\n"
     "3. Spotify search link\n"
     "Format the response cleanly using bullet points."
     ),
    
    ("user",
     "Language: {language}\nMusic Type: {musictype}\n Singer :{singer}"
     "Give me the best 10- 15 songs.")
])


chain = prompt|llm|StrOutputParser()

user_language = st.text_input("🎤 Enter music language ")

singer_name = st.text_input("Enter Singer name")

music_types = [
    "Lo-fi",
    "Romantic",
    "Sad",
    "Happy",
    "Chill",
    "Relaxing",
    "Meditation",
    "Focus / Study",
    "Workout",
    "Party",
    "Devotional",
    "Classical",
    "Ambient",
    "Nature Sounds"
]

music_type = st.selectbox("🎶 Select music type:", music_types)


if st.button("🔍 Search"):
    if not user_language or not music_type or not singer_name:
        st.error("❗ Please select options first .")
    else:
        with st.spinner("🎧 Fetching top songs..."):
            result = chain.invoke({"language": user_language, "musictype": music_type , "singer" : singer_name})
            st.markdown(result)
