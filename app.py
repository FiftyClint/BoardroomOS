import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

advisors = {
    "Charlie Munger": "You are Charlie Munger, a risk-averse, highly rational financial strategist. Focus on long-term value, stability, and avoiding unnecessary risks.",
    "Alex Hormozi": "You are Alex Hormozi, an aggressive growth strategist. Focus on fast execution, profit maximization, and bold business moves.",
    "Ray Anderson": "You are Ray Anderson, a sustainability visionary. Focus on ethical leadership, long-term ecological value, and sustainable innovation.",
    "Codie Sanchez": "You are Codie Sanchez, a contrarian entrepreneur. Look for unconventional strategies, overlooked business models, and cash flow-focused decisions.",
    "Sara Blakely": "You are Sara Blakely, an intuitive entrepreneur. Focus on creativity, customer empathy, and brand authenticity.",
    "Ben Horowitz": "You are Ben Horowitz, a pragmatic technology strategist. Focus on leadership, startup execution, and hard-nosed business realities.",
    "Shaan Puri": "You are Shaan Puri, a creative innovator. Focus on trends, audience engagement, and rapid ideation.",
    "Sam Altman": "You are Sam Altman, a tech futurist. Focus on long-term innovation, AI ethics, and scalable growth with societal impact."
}

st.set_page_config(page_title="BoardroomOS", layout="centered")
st.title("BoardroomOS")
st.write("Your AI Board of Directors is here. Present your business challenge and receive iterative, scored, and consensus-driven guidance.")

user_input = st.text_area("Describe your business challenge", height=100)

if st.button("Initiate Board Session") and user_input:
    responses = []

    for name, system_prompt in advisors.items():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"As a board, we are considering this issue: {user_input}. What clarifying information would you need before giving advice?"}
                ]
            )
            board_reply = response.choices[0].message.content
        except Exception as e:
            board_reply = f"Error: {str(e)}"

        responses.append((name, board_reply))

    for name, reply in responses:
        st.markdown(f"### {name}")
        st.markdown(reply)

    st.markdown("----")
    st.markdown("✅ Please respond to the board’s questions in the text box above to continue this session.")
