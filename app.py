# app.py - Professor Ali Bazrafkan's AI Assistant
# API key is stored in Streamlit Secrets, NOT in this file

import streamlit as st
from groq import Groq

st.set_page_config(page_title="Professor Bazrafkan's AI Assistant", page_icon="🎓")
st.title("🎓 Professor Ali Bazrafkan")
st.caption("Assistant Professor of Precision Agriculture | Montana State University")

# Load API key from secrets (safe - no key hardcoded)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# Knowledge base
knowledge = """
Professor Ali Bazrafkan - Montana State University
Assistant Professor of Precision Agriculture
Email: ali.bazrafkan@montana.edu
Office: Plant Sciences Building, Room 218
Office Hours: Tuesdays & Thursdays 2-4 PM
Research: Computer vision, YOLO object detection, plant phenotyping

PSCI456 Course - Precision Agriculture Technologies
Topics: YOLO v5-v12, segmentation, plant phenotyping, UAV imagery
Lab: Thursdays 1-4 PM, Computer Lab
Software: Python, PyTorch, YOLO, OpenCV

PACV Lab Equipment: NVIDIA RTX 4090 GPUs (4 units), DJI Phantom 4 drone, Sony cameras

Assignments:
Assignment 1: YOLO Installation (Due: February 10)
Assignment 2: Dataset Annotation (Due: March 3)
Assignment 3: Training YOLO (Due: March 24)
Final Project: Due Finals Week
"""

def get_answer(question):
    prompt = f"""You are an AI assistant for Professor Ali Bazrafkan at Montana State University.

Answer using ONLY the information below. If the answer is not there, politely say:
"I'm sorry, I don't have that information in Professor Bazrafkan's course materials."

INFORMATION:
{knowledge}

QUESTION: {question}

ANSWER:"""
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

# Chat interface
st.subheader("💬 Ask me anything")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching Professor Bazrafkan's materials..."):
            response = get_answer(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.markdown("### 📚 Knowledge Base")
    st.markdown("**Includes:** Professor Bio, Course Info, Lab Equipment, Assignments")
    st.markdown("---")
    st.markdown("### 🔧 Try asking:")
    st.markdown("- What is your research focus?")
    st.markdown("- What equipment is in the lab?")
    st.markdown("- When is Assignment 1 due?")
    st.markdown("- When are office hours?")