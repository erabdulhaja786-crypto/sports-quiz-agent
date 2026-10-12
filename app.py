
import streamlit as st
from pathlib import Path

from src.generator import compile_quiz_data
from src.database import setup_and_populate_db


# =====================================================
# 1. PAGE CONFIGURATION
# Must be the first Streamlit command.
# =====================================================
st.set_page_config(
    page_title="AI Sports Quiz Arena",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# 2. LOAD CUSTOM CSS
# style.css must be in the same folder as app.py.
# =====================================================
css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    css_content = css_path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css_content}</style>",
        unsafe_allow_html=True,
    )


# =====================================================
# 3. HERO BANNER
# =====================================================
st.markdown(
    """
    <div style="
        padding: 32px;
        margin-bottom: 25px;
        border-radius: 20px;
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.28),
                transparent 40%
            ),
            linear-gradient(120deg, #111C32, #0B1020);
        border: 1px solid rgba(0, 229, 255, 0.35);
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
            margin: 14px 0 8px 0;
            font-size: clamp(30px, 4vw, 44px);
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
# 4. INITIALIZE KNOWLEDGE BASE
# =====================================================
@st.cache_resource
def prepare_knowledge_base():
    return setup_and_populate_db()


with st.spinner("Preparing the sports knowledge arena..."):
    prepare_knowledge_base()


# =====================================================
# 5. SIDEBAR — ARENA CONTROL
# =====================================================
st.sidebar.markdown(
    """
    <div style="
        padding: 15px;
        margin-bottom: 18px;
        border-radius: 14px;
        background: linear-gradient(120deg, #14223A, #101629);
        border: 1px solid rgba(0, 229, 255, 0.30);
    ">
        <div style="
            color: #00E5FF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
        ">
            ARENA CONTROL
        </div>
        <div style="
            color: #FFFFFF;
            font-size: 22px;
            font-weight: 700;
            margin-top: 6px;
        ">
            Quiz Settings
        </div>
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
    value="Easy",
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Groq • ChromaDB • Web Search")


# =====================================================
# 6. SESSION STATE
# Preserve the last generated quiz across reruns.
# =====================================================
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None

if "quiz_context" not in st.session_state:
    st.session_state.quiz_context = None

if "quiz_sport" not in st.session_state:
    st.session_state.quiz_sport = None

if "quiz_difficulty" not in st.session_state:
    st.session_state.quiz_difficulty = None


# =====================================================
# 7. MAIN CONTENT
# =====================================================
st.markdown("### 🎯 Your Next Challenge")

st.write(
    "Choose a sport and difficulty in the sidebar, "
    "then generate a fresh AI-powered quiz."
)

if st.sidebar.button(
    "⚡ Generate Fresh Quiz",
    use_container_width=True,
    type="primary",
):
    with st.spinner(
        "Fetching sports facts and searching the live web..."
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
# 8. DISPLAY GENERATED QUIZ
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

    st.download_button(
        label="📥 Download Quiz",
        data=st.session_state.quiz_output,
        file_name="sports_quiz.txt",
        mime="text/plain",
        use_container_width=True,
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
            padding: 35px 24px;
            text-align: center;
            border-radius: 18px;
            background:
                radial-gradient(
                    circle at 50% 0%,
                    rgba(0, 229, 255, 0.08),
                    transparent 65%
                ),
                linear-gradient(145deg, #111A2E, #0B1020);
            border: 1px solid rgba(124, 145, 190, 0.25);
        ">
            <div style="font-size: 48px;">🏟️</div>

            <div style="
                font-size: 23px;
                font-weight: 750;
                color: #F1F5FF;
                margin: 12px 0;
            ">
                The Arena Is Ready
            </div>

            <div style="
                color: #AAB9D3;
                font-size: 15px;
            ">
                Choose your sport and difficulty.
                Generate your challenge and test your knowledge.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# 9. FOOTER
# =====================================================
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        color: #8190AD;
        font-size: 12px;
        padding: 8px;
    ">
        🏆 AI SPORTS QUIZ ARENA
        &nbsp;•&nbsp; Powered by Groq, ChromaDB & Web Search
    </div>
    """,
    unsafe_allow_html=True,
)
