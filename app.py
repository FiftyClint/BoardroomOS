import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

advisors = {
    "Charlie Munger": "You are Charlie Munger, the chairperson of the board. Consolidate feedback, moderate disputes, and summarize the board’s progress. Push for consensus. Score only after evaluating all board input.",
    "Alex Hormozi": "You are Alex Hormozi, focused on monetization, scaling, and customer acquisition. Be direct, tactical, and iterate quickly.",
    "Ray Anderson": "You are Ray Anderson, focused on long-term sustainable value, eco-conscious practices, and triple bottom line thinking.",
    "Codie Sanchez": "You are Codie Sanchez, a contrarian, acquisition-driven thinker. Look for underutilized assets and profitability levers.",
    "Sara Blakely": "You are Sara Blakely, customer-first, creative, and intuitive. Focus on simplicity, empathy, and brand authenticity.",
    "Ben Horowitz": "You are Ben Horowitz, pragmatic, leadership-focused, and execution-oriented. Consider culture, systems, and crisis strategy.",
    "Shaan Puri": "You are Shaan Puri, idea arbitrageur and momentum hunter. Identify signals, rapid testing paths, and audience-first leverage.",
    "Sam Altman": "You are Sam Altman, focused on scalable innovation, AI, defensibility, and long-term future bets. Ground all ideas in first-principles logic."
}

st.set_page_config(page_title="BoardroomOS", layout="centered")
st.title("BoardroomOS")
st.write("Your AI board of directors will simulate discussion and iterate together until they reach consensus. Scoring is based on: Capital Allocation, Market Advantage, and Business Model Confidence. The session ends only when every advisor scores ≥8/10 in all three categories.")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "round" not in st.session_state:
    st.session_state.round = 0
if "advisor_feedback" not in st.session_state:
    st.session_state.advisor_feedback = {}
if "iteration_summary" not in st.session_state:
    st.session_state.iteration_summary = ""

# Handle clearing/reset flag
if st.session_state.get("user_text_input_reset"):
    st.session_state["user_text_input"] = ""
    del st.session_state["user_text_input_reset"]

user_input = st.text_area("Describe your business challenge or respond to the board:", height=100, key="user_text_input")

if st.button("Continue Board Session") and st.session_state.get("user_text_input", "").strip():
    user_input = st.session_state["user_text_input"]
    st.session_state.chat_log.append(("You", user_input))
    advisor_messages = []

    for name, persona in advisors.items():
        # Build context including previous advisor comments
        thread = ""
        for prior_name, prior_msg in st.session_state.chat_log[-len(advisors):]:
            if prior_name != name:
                thread += f"{prior_name}: {prior_msg}\n"

        prompt = f"Round {st.session_state.round}:\n\nBusiness challenge: {user_input}\n\nOther board members have said:\n{thread}\n\nPlease respond with:\n1. Your next recommendation (as yourself).\n2. A score for Capital Allocation (1–10)\n3. A score for Market Advantage (1–10)\n4. A score for Business Model Confidence (1–10)\n5. What would need to improve to raise all 3 scores to at least 8/10."

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": persona},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"

        st.session_state.chat_log.append((name, reply))
        advisor_messages.append((name, reply))

    st.session_state.round += 1
    st.session_state["user_text_input_reset"] = True
    st.experimental_rerun()

# Display entire boardroom discussion
st.markdown("## Boardroom Session Log")
for name, msg in st.session_state.chat_log:
    st.markdown(f"**{name}**: {msg}")
