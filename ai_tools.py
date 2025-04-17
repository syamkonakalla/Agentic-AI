# streamlit_agentic_ai.py

import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Streamlit app layout
st.title("🧠 Agentic AI Playground")
st.sidebar.title("Agent Configuration")

model_choice = st.sidebar.selectbox("Select Model", ["Groq", "OpenAI"])
tool_choice = st.sidebar.multiselect("Select Tools", ["DuckDuckGoTools", "Calculator"])
tone_choice = st.sidebar.selectbox("Agent Tone", ["Polite", "Humorous", "Techy"])

# Tool setup
tools = []
if "DuckDuckGoTools" in tool_choice:
    tools.append(DuckDuckGoTools())

# Model selection
if model_choice == "Groq":
    model = Groq(id="llama-3.1-8b-instant")
else:
    model = OpenAIChat()

# Tone setup
if tone_choice == "Polite":
    description = "Hello! I'm a helpful assistant. How may I assist you today?"
elif tone_choice == "Humorous":
    description = "Yo! I'm your AI buddy – answers served with a side of laughs!"
else:
    description = "I'm your tech-savvy agent, ready to dig deep and deliver insights."

agent = Agent(
    model=model,
    description=description,
    tools=tools,
    show_tool_calls=True,
    markdown=True
)

st.markdown("## Ask Me Anything")
query = st.text_input("Your Query")

if st.button("Run Agent"):
    if query:
        with st.spinner("Thinking..."):
            response = agent.run(query)
        st.markdown(response)

# Additional features
st.markdown("## ✨ Additional Features")

col1, col2 = st.columns(2)

with col1:
    with st.expander("🔍 Research Agent: Summarize Topic"):
        topic = st.text_input("Enter topic to research", key="research")
        if st.button("Summarize", key="btn_research"):
            if topic:
                info = agent.run(f"Search and summarize about {topic}")
                st.markdown(info)

    with st.expander("📰 News Summarizer"):
        event = st.text_input("Enter current event", key="news")
        if st.button("Summarize News", key="btn_news"):
            if event:
                summary = agent.run(f"Summarize top 3 news articles on: {event}")
                st.markdown(summary)

    with st.expander("📝 Auto-Fill Resume"):
        name = st.text_input("Your Name", key="resume")
        skills = st.text_input("Your Skills")
        role = st.text_input("Role You're Applying For")
        if st.button("Generate Resume"):
            if name and skills and role:
                resume = agent.run(f"Create resume for {name}, role: {role}, skills: {skills}")
                st.markdown(resume)

with col2:
    with st.expander("🧮 Multi-Tool Decision Agent"):
        decision_query = st.text_input("Enter question", key="decision")
        if st.button("Decide", key="btn_decide"):
            if decision_query:
                result = agent.run(decision_query)
                st.markdown(result)

    with st.expander("💼 Domain-Specific Assistant (Tech)"):
        topic_tech = st.text_input("Tech Query", key="domain")
        if st.button("Answer Tech Query"):
            if topic_tech:
                tech_result = agent.run(f"As a tech expert, answer this: {topic_tech}")
                st.markdown(tech_result)

    with st.expander("💬 Feedback-Improving Agent"):
        question = st.text_input("Ask something for feedback mode", key="feedback")
        if st.button("Get Answer and Feedback"):
            if question:
                reply = agent.run(question)
                st.markdown(reply)
                feedback = st.radio("Was this helpful?", ["Yes", "No"])
                if feedback == "No":
                    st.warning("Thanks! I'll try to improve next time.")

    with st.expander("🤖 Multi-Agent Collaboration"):
        topic = st.text_input("Topic for collaboration", key="collab")
        if st.button("Collaborate"):
            if topic:
                output = agent.run(f"Let one agent fact-check and another write a blog on: {topic}")
                st.markdown(output)