import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Full advisor personas — no shortcuts
advisors = {
    "Charlie Munger": "You are Charlie Munger, the chairperson of the board. Consolidate feedback, moderate disputes, and summarize the board’s progress. Push for consensus. Score only after evaluating all board input. Use mental models like inversion, cost-benefit analysis, and margin of safety.",
    "Alex Hormozi": "You are Alex Hormozi, focused on monetization, scaling, and customer acquisition. Be direct, tactical, and iterate quickly. Use value-based pricing, MVPs, and high-ROI thinking.",
    "Ray Anderson": "You are Ray Anderson, focused on long-term sustainable value, eco-conscious practices, and triple bottom line thinking. You prioritize impact, ethics, and lifecycle value.",
    "Codie Sanchez": "You are Codie Sanchez, a contrarian, acquisition-driven thinker. Look for underutilized assets, cash flow, boring businesses, and profitability levers others miss.",
    "Sara Blakely": "You are Sara Blakely, customer-first, creative, and intuitive. Focus on simplicity, empathy, storytelling, and authentic brand connection.",
    "Ben Horowitz": "You are Ben Horowitz, pragmatic, leadership-focused, and execution-oriented. Evaluate company culture, scalability, leadership, and wartime vs. peacetime CEO dynamics.",
    "Shaan Puri": "You are Shaan Puri, idea arbitrageur and momentum hunter. Spot early trends, use frameworks, and prioritize audience-first growth with speed and creativity.",
    "Sam Altman": "You are Sam Altman, focused on scalable innovation, defensibility, and long-term societal impact. Evaluate market size, moat, and bold future bets using first-principles thinking."
}

# Set up UI
st.set_page_config(page_title="BoardroomOS", layout="centered")
st.title("BoardroomOS")
st.write("Your AI board of directors will simulate discussion and iterate together until consensus is reached. Scoring is based on: Capital Allocation, Market Advantage, and Business Model Confidence.")

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "round" not in st.session_state:
    st.session_state.round = 0

# User input — uncontrolled input field (no key)
user_input = st.text_area("Describe your business challenge or respond to the board:", height=100)

# Button click behavior
if st.button("Continue Board Session") and user_input.strip():
    st.session_state.chat_log.append(("You", user_input))

    for name, persona in advisors.items():
        thread = ""
        for prior_name, prior_msg in st.session_state.chat_log[-len(advisors):]:
            if prior_name != name:
                thread += f"{prior_name}: {prior_msg}\n"

        prompt = f"""Round {st.session_state.round}:

Business challenge: {user_input}

Other board members have said:
{thread}

Please respond with:
1. Your next recommendation (as yourself).
2. A score for Capital Allocation (1–10)
3. A score for Market Advantage (1–10)
4. A score for Business Model Confidence (1–10)
5. What would need to improve to raise all 3 scores to at least 8/10.
"""

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

    st.session_state.round += 1
    # NOTE: We do NOT rerun, and we do NOT reset the text field forcibly.
    # The user can edit or submit again naturally.

# Session log
st.markdown("## Boardroom Session Log")
for name, msg in st.session_state.chat_log:
    st.markdown(f"**{name}**: {msg}")
