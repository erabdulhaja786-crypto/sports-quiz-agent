
import streamlit as st
from pathlib import Path

from src.generator import compile_quiz_data
from src.database import setup_and_populate_db


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="AI Sports Quiz Arena",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# 2. LOAD CSS
# =====================================================
css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# =====================================================
# 3. HERO BANNER - NATIVE STREAMLIT
# =====================================================
st.caption("RAG POWERED | LIVE SPORTS INTELLIGENCE")
st.title("🏆 ENTER THE ARENA")
st.write(
    "Test your knowledge. Beat the challenge. "
    "Own the scoreboard."
)
st.divider()


# =====================================================
# 4. INITIALIZE KNOWLEDGE BASE
# =====================================================
@st.cache_resource
def prepare_knowledge_base():
    return setup_and_populate_db()


with st.spinner("Preparing the sports knowledge arena..."):
    try:
        prepare_knowledge_base()
    except Exception as e:
        st.error(f"Failed to initialize knowledge base: {e}")
        st.stop()


# =====================================================
# 5. SIDEBAR SETTINGS
# =====================================================
st.sidebar.caption("ARENA CONTROL")
st.sidebar.title("Quiz Settings")

sport_choice = st.sidebar.selectbox(
    "🏅 Select Sport",
    ["Cricket", "Football", "Badminton"],
)

difficulty = st.sidebar.select_slider(
    "⚡ Select Difficulty",
    options=["Easy", "Medium", "Hard"],
    value="Easy",
)

st.sidebar.divider()
st.sidebar.caption("Powered by Groq | ChromaDB | Web Search")


# =====================================================
# 6. SESSION STATE
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
# 7. CHALLENGE SECTION
# =====================================================
st.subheader("🎯 Your Next Challenge")
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

            if not quiz_text:
                st.warning("The generator returned an empty quiz.")
            else:
                st.session_state.quiz_output = quiz_text
                st.session_state.quiz_context = context_used
                st.session_state.quiz_sport = sport_choice
                st.session_state.quiz_difficulty = difficulty
                st.success("🏆 Your quiz is ready!")

        except Exception as e:
            st.error(f"Failed to generate quiz: {e}")


# =====================================================
# 8. QUIZ OUTPUT
# =====================================================
if st.session_state.quiz_output:
    quiz_sport = st.session_state.quiz_sport or sport_choice
    quiz_difficulty = (
        st.session_state.quiz_difficulty or difficulty
    )

    st.subheader(f"🏆 {quiz_sport} Arena")
    st.caption(f"Difficulty: {quiz_difficulty}")

    st.text_area(
        "📝 Generated Quiz - Copy and Share",
        value=st.session_state.quiz_output,
        height=350,
        key="generated_quiz_display",
    )

    st.download_button(
        "📥 Download Quiz",
        data=st.session_state.quiz_output,
        file_name=f"{quiz_sport.lower()}_quiz.txt",
        mime="text/plain",
        use_container_width=True,
    )

    with st.expander("🔍 Inspect Ground Truth (RAG Context Used)"):
        context = st.session_state.quiz_context or ""

        if context:
            st.code(context, language="markdown")
        else:
            st.info("No RAG context was returned by the generator.")

else:
    st.info(
        "🏟️ **The Arena Is Ready**\n\n"
        "Choose your sport and difficulty. "
        "Generate your challenge and test your knowledge."
    )


# =====================================================
# 9. FOOTER
# =====================================================
st.divider()
st.caption(
    "🏆 AI SPORTS QUIZ ARENA | "
    "Powered by Groq, ChromaDB and Web Search"
)
