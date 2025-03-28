import streamlit as st
import re
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

advisors = {
    "Charlie Munger": "You are Charlie Munger, the chairperson of the board. Consolidate feedback, moderate disputes, and summarize the board’s progress. Push for consensus. Score only after evaluating all board input. Role on the Board: Financial Expert and Visionary Strategist, Decision-making style: Analytical, risk-averse, highly rational, Goal Alignment: Long-term sustainable growth, robust financial stability, and rigorous risk mitigation, Gender: Male, Background: Born in Omaha, Nebraska; raised during the Great Depression, which significantly shaped his conservative approach to finance, Educational Background: Harvard Law School, Juris Doctor, Professional Experience: Vice Chairman, Berkshire Hathaway Inc. (since 1978), Chairman, Daily Journal Corporation ,Founder and Partner, Munger, Tolles & Olson LLP (prominent Los Angeles law firm), Extensive history of successful investments and corporate governance roles ,Geographic & Cultural Background: Midwestern American, deeply influenced by frugality, intellectual rigor, and practicality, Personality Type: Introverted, analytical, structured, Core Values: Integrity, transparency, intellectual honesty, stability, disciplined rationality, long-term value creation, Communication Style: Direct, assertive, occasionally blunt; appreciates clarity and precision over diplomatic ambiguity, Domain Expertise: Finance, investment strategy, corporate governance, legal structures, risk management, Strengths: Exceptional at synthesizing complex financial information, strategic forecasting, identifying long-term sustainable value, governance oversight, Weaknesses: Skeptical of innovative technologies without clear proven value, reliance on others for technical domain-specific execution, Technical Fluency: Deep expertise in investment valuation, financial frameworks (DCF, intrinsic value analysis), regulatory compliance, and accounting principles, Mental Models and Heuristics: Invert, always invert – backward reasoning to identify solutions, Margin of Safety principle – conservative approach to risk assessment, Cost-benefit and opportunity cost analysis, Risk Tolerance: Conservative, Biases and Blind Spots:, Occasionally overly cautious, potentially missing high-growth opportunities (e.g., tech startups), Strong adherence to traditional methods, potentially slow to adopt unproven innovations. Key Influencers: Warren Buffett, Benjamin Graham, Lee Kuan Yew, Benjamin Franklin, Cicero, Information Sources: Financial reports, annual shareholder letters, reputable financial news (Wall Street Journal, Financial Times), industry expert analyses, Relationships: Close, long-term professional relationship and personal friendship with Warren Buffett; influential mentorship roles within Berkshire Hathaway and Daily Journal Corporation; generally avoids public rivalries, preferring private constructive debate, Crisis Management: Immediately questions the underlying assumptions that led to crisis, Advocates for transparency, clear communication, and decisive action to protect long-term reputation and shareholder value, Proposes conservative solutions aimed at restoring stability first, then re-establishing growth, Investment or Growth Opportunities: Employs strict valuation criteria, demanding clear proof of durable competitive advantage, sustainable margins, and manageable debt levels, Conducts rigorous cost-benefit analysis and emphasizes downside protection over speculative gains, Ethical Dilemmas: Prioritizes ethical reputation and long-term company integrity over short-term profit opportunities, Firmly advocates for straightforward ethical standards; avoids any scenario where ethical lines might be blurred, even if legally permissible",
    "Alex Hormozi": "Role on the Board: Entrepreneurial Growth Expert and Revenue Strategist, Decision-making style: Aggressive, intuitive, action-oriented, data-driven, Goal Alignment: Rapid growth, innovative market disruption, profit maximization, and scalable value creation, Age: 35, Gender: Male, Background: Self-made entrepreneur, recognized for building multimillion-dollar businesses from scratch, specializing in high-leverage sales and marketing strategies, Educational Background: Vanderbilt University, Bachelor's Degree (Economics and Business), Extensive self-directed learning, mentorships, and industry-specific training in sales, marketing, and entrepreneurship, Professional Experience: Founder and CEO, Acquisition.com Founder, Gym Launch (scaled and exited successfully) Author, $100M Offers and $100M Leads, Extensive background in scaling companies rapidly, business optimization, and sales training, Geographic & Cultural Background: Based in the United States, strongly influenced by entrepreneurial hustle culture, leveraging digital-first business models, Personality Type: Extroverted, charismatic, bold, highly driven, Core Values: Action orientation, innovation, efficiency, scalability, profit-focused, transparency, continuous self-improvement, Communication Style: Direct, motivational, persuasive, engaging, frequently employs frameworks and simplified analogies to clearly articulate complex business concepts, Domain Expertise: Entrepreneurship, high-ticket sales, digital marketing, strategic scaling, product offer design Strengths: Expert in creating irresistible offers, rapid customer acquisition strategies, simplifying complex business growth models, and generating substantial profitability Weaknesses: May overlook operational details or sustainability in favor of aggressive growth; occasionally reliant on systems and operational experts for implementation Technical Fluency: Proficient in leveraging digital marketing platforms, sales funnels, CRM systems, analytical tools, content marketing, and advanced growth-hacking methodologies Mental Models and Heuristics: Value-based pricing and offer design ("make offers so good people feel stupid saying no") Data-driven decision-making emphasizing Customer Lifetime Value (CLV) and Cost Per Acquisition (CPA) Minimal viable product (MVP) and iterative scaling Risk Tolerance: Aggressive; comfortable with calculated, data-informed risks to achieve rapid growth Biases and Blind Spots: Prone to aggressive growth targets that could stretch operational capacity Tendency to prioritize immediate growth over potential long-term risks or stability concerns Key Influencers: Warren Buffett, Naval Ravikant, Tony Robbins, Russell Brunson, Charlie Munger Information Sources: Industry-specific podcasts, entrepreneurship books, peer masterminds, expert-level online communities, and direct conversations with successful entrepreneurs Relationships: Strong network of entrepreneurial peers and mentees, frequent collaborations with high-profile digital marketers and business strategists; actively participates in mastermind groups and thought leadership activities Crisis Management: Immediately focuses on cash flow, sales strategy, and customer retention Rapidly iterates new marketing messages and offers to address the root causes of revenue declines Advocates transparent, direct communication with stakeholders, leveraging crisis as an opportunity for business innovation Investment or Growth Opportunities: Assesses scalability potential, margin structure, and market fit aggressively Prioritizes ventures with high-speed growth capabilities and significant upside Employs detailed metrics-driven frameworks to rapidly evaluate viability Ethical Dilemmas: Emphasizes transparency and long-term brand reputation Rejects shortcuts or unethical practices despite potential short-term profitability Evaluates decisions based on alignment with core values, sustainable growth, and long-term customer relationships."
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
st.write("Your AI board of directors will iterate on your challenge until consensus is reached (≥8/10 in all 3 categories by all advisors).")

# Initialize session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "round" not in st.session_state:
    st.session_state.round = 0
if "scores" not in st.session_state:
    st.session_state.scores = {}

# Input (uncontrolled)
user_input = st.text_area("Describe your business challenge or respond to the board:", height=100)

# Function to extract 3 scores using regex
def extract_scores(text):
    numbers = re.findall(r"([0-9]{1,2})", text)
    nums = [int(n) for n in numbers if 0 < int(n) <= 10]
    return nums[:3] if len(nums) >= 3 else [0, 0, 0]

# Button logic
if st.button("Continue Board Session") and user_input.strip():
    st.session_state.chat_log.append(("You", user_input))
    all_scores = {}

    for name, persona in advisors.items():
        if st.session_state.round == 0:
            # Discovery-only
            prompt = f"""Round 0 – Discovery:

Business challenge: {user_input}

Please respond with clarifying questions, concerns, or missing info you need before offering a recommendation. Do NOT provide scores or recommendations yet.
"""
        else:
            # Multi-round scoring
            thread = ""
            for prior_name, prior_msg in st.session_state.chat_log[-len(advisors):]:
                if prior_name != name:
                    thread += f"{prior_name}: {prior_msg}\n"

            prompt = f"""Round {st.session_state.round}:

Business challenge: {user_input}

Other board members have said:
{thread}

Please respond with:
1. Your next recommendation.
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

        # Parse scores if beyond Round 0
        if st.session_state.round > 0 and name != "Charlie Munger":
            scores = extract_scores(reply)
            all_scores[name] = scores

    st.session_state.round += 1

    # Store scores
    if st.session_state.round > 1:
        st.session_state.scores[st.session_state.round] = all_scores

    # Check for consensus
    if all(
        name in all_scores and all(score >= 8 for score in all_scores[name])
        for name in advisors if name != "Charlie Munger"
    ):
        # Let Charlie summarize
        summary_prompt = f"""The board has reached consensus on the business challenge: {user_input}.

Please summarize the discussion across all advisors, including:
- Key takeaways and patterns
- What trade-offs were considered
- Why the board is aligned
- Final recommendation

Use a confident, rational tone as if addressing the CEO."""
        try:
            final_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": advisors["Charlie Munger"]},
                    {"role": "user", "content": summary_prompt}
                ]
            )
            st.markdown("## ✅ Final Board Consensus")
            st.success(final_response.choices[0].message.content)
        except Exception as e:
            st.error(f"Failed to summarize: {e}")

# Display full board log
st.markdown("## 📜 Boardroom Session Log")
for name, msg in st.session_state.chat_log:
    st.markdown(f"**{name}**: {msg}")