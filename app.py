
import streamlit as st
from pathlib import Path

from src.generator import compile_quiz_data
from src.database import setup_and_populate_db


# =====================================================
# 1. PAGE CONFIGURATION — MUST BE FIRST STREAMLIT CALL
# =====================================================
st.set_page_config(
    page_title="AI Sports Quiz Arena",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# 2. LOAD MIDNIGHT ARENA CSS
# =====================================================
css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# =====================================================
# 3. INITIALIZE KNOWLEDGE BASE
# =====================================================
@st.cache_resource
def prepare_knowledge_base():
    return setup_and_populate_db()


with st.spinner("Preparing the sports knowledge arena..."):
    prepare_knowledge_base()


# =====================================================
# 4. PREMIUM HERO BANNER
# =====================================================
st.markdown(
    """
    <div style="
        padding: 30px;
        margin-bottom: 24px;
        border-radius: 20px;
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.30),
                transparent 38%
            ),
            linear-gradient(120deg, #111C32, #0B1020);
        border: 1px solid rgba(0, 229, 255, 0.30);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    ">
        <div style="
            color: #00E5FF;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 3px;
        ">
            RAG POWERED • LIVE SPORTS INTELLIGENCE
        </div>

        <h1 style="
            margin: 12px 0 8px 0;
            font-size: clamp(28px, 4vw, 42px);
            color: #FFFFFF;
        ">
            🏆 ENTER THE ARENA
        </h1>

        <p style="
            color: #B7C5DF;
            font-size: 16px;
            margin-bottom: 0;
        ">
            Test your knowledge. Beat the challenge.
            Own the scoreboard.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# 5. SIDEBAR SETTINGS
# =====================================================
st.sidebar.markdown(
    """
    <div style="
        padding: 12px;
        border-radius: 12px;
        background: linear-gradient(120deg, #14223A, #101629);
        border: 1px solid rgba(0, 229, 255, 0.25);
        margin-bottom: 18px;
    ">
        <div style="
            color: #00E5FF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
        ">ARENA CONTROL</div>
        <div style="
            color: #FFFFFF;
            font-size: 21px;
            font-weight: 700;
            margin-top: 5px;
        ">Quiz Settings</div>
    </div>
    """,
    unsafe_allow_html=True,
)

sport_choice = st.sidebar.selectbox(
    "🏅 Select Sport",
    ["Cricket", "Football", "Badminton"],
)

difficulty = st.sidebar.select_slider(
    "⚡ Select Difficulty",
    options=["Easy", "Medium", "Hard"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Groq • ChromaDB • Web Search")


# =====================================================
# 6. SESSION STATE
# =====================================================
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None
    st.session_state.quiz_sport = None
    st.session_state.quiz_difficulty = None


# =====================================================
# 7. GENERATE QUIZ
# =====================================================
st.markdown("### 🎯 Your Next Challenge")
st.write(
    "Choose your sport and difficulty in the sidebar, "
    "then generate a fresh AI-powered quiz."
)

if st.sidebar.button(
    "⚡ Generate Fresh Quiz",
    use_container_width=True,
):
    with st.spinner(
        "Fetching sports facts and searching live web sources..."
    ):
        try:
            quiz_text, context_used = compile_quiz_data(
                sport_choice,
                difficulty,
            )

            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            st.session_state.quiz_sport = sport_choice
            st.session_state.quiz_difficulty = difficulty

            st.success("🏆 Your quiz is ready!")

        except Exception as e:
            st.error(f"Failed to generate quiz: {e}")


# =====================================================
# 8. DISPLAY QUIZ
# =====================================================
if st.session_state.quiz_output:
    st.markdown(
        f"### 🏆 {st.session_state.quiz_sport} Arena"
    )

    st.caption(
        f"Difficulty: {st.session_state.quiz_difficulty}"
    )

    st.text_area(
        "📝 Generated Quiz — Copy and Share",
        value=st.session_state.quiz_output,
        height=350,
    )

    with st.expander(
        "🔍 Inspect Ground Truth (RAG Context Used)"
    ):
        st.code(
            st.session_state.quiz_context or "",
            language="markdown",
        )

else:
    st.markdown(
        """
        <div style="
            padding: 28px;
            text-align: center;
            border-radius: 16px;
            background: linear-gradient(145deg, #111A2E, #0B1020);
            border: 1px solid rgba(124, 145, 190, 0.25);
        ">
            <div style="font-size: 42px;">🏟️</div>
            <div style="
                font-size: 21px;
                font-weight: 700;
                color: #F1F5FF;
                margin: 10px 0;
            ">The Arena Is Ready</div>
            <div style="color: #AAB9D3;">
                Select your sport and difficulty, then generate
                your first challenge.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
