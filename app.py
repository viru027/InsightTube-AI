import streamlit as st

from core.extractor import VideoExtractor
from core.transcriber import Transcriber
from core.rag_engine import RAGEngine

st.set_page_config(
    page_title="InsightTube AI",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 InsightTube AI")
st.caption("AI-Powered Video Intelligence Platform")

# -----------------------------
# Session State
# -----------------------------
if "video" not in st.session_state:
    st.session_state.video = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "segments" not in st.session_state:
    st.session_state.segments = None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "",
    [
        "Analyze Video",
        "AI Chat"
    ]
)

# ==============================
# Analyze Video
# ==============================

if page == "Analyze Video":

    st.subheader("Analyze YouTube Video")

    url = st.text_input(
        "Paste YouTube URL",
        placeholder="https://youtube.com/watch?v=..."
    )

    if st.button("Analyze Video", use_container_width=True):

        if not url:
            st.warning("Please enter a YouTube URL.")
            st.stop()

        with st.spinner("Downloading video audio..."):

            extractor = VideoExtractor()

            data = extractor.process(url)

        with st.spinner("Transcribing using Whisper..."):

            transcriber = Transcriber()

            transcript_data = transcriber.transcribe(
                data["audio_path"]
            )

        with st.spinner("Creating searchable knowledge base..."):

            rag = RAGEngine()

        try:
            rag.index_video(
            video_id=data["video"]["id"],
            transcript=transcript_data["transcript"]
        )

        except ValueError as e:
            st.warning(str(e))
            st.stop()

        st.session_state.video = data["video"]
        st.session_state.video_id = data["video"]["id"]
        st.session_state.transcript = transcript_data["transcript"]
        st.session_state.segments = transcript_data["segments"]

        st.success("Video processed successfully!")

    if st.session_state.video:

        video = st.session_state.video

        st.image(video["thumbnail"], width=400)

        st.subheader(video["title"])

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Channel:**", video["channel"])
            st.write("**Duration:**", video["duration"], "seconds")

        with col2:
            st.write("**Views:**", f"{video['view_count']:,}")
            st.write("**Upload Date:**", video["upload_date"])

        with st.expander("Transcript"):
            st.write(st.session_state.transcript)

# ==============================
# # ==============================
# AI Chat
# ==============================

elif page == "AI Chat":

    st.subheader("💬 Chat with Video")

    if st.session_state.video is None:
        st.warning("Please analyze a YouTube video first.")
        st.stop()

    from core.chat_engine import ChatEngine

    rag = RAGEngine()
    chat = ChatEngine()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -----------------------------
    # AI Learning Modes
    # -----------------------------

    st.markdown("### 🧠 AI Learning Mode")

    ai_mode = st.selectbox(
        "Choose Mode",
        [
            "Ask Questions",
            "Video Summary",
            "Explain Simply",
            "Project Ideas",
            "Interview Questions",
            "Quiz Generator",
            "Learning Roadmap",
            "Coding Challenges",
            "Resume Project Builder",
            "Research Topics"
        ]
    )

    mode_description = {
        "Ask Questions": "Ask anything about the video.",
        "Video Summary": "Generate a concise summary.",
        "Explain Simply": "Explain concepts in beginner-friendly language.",
        "Project Ideas": "Generate practical project ideas.",
        "Interview Questions": "Generate interview questions.",
        "Quiz Generator": "Generate MCQs with answers.",
        "Learning Roadmap": "Create a learning roadmap.",
        "Coding Challenges": "Generate coding exercises.",
        "Resume Project Builder": "Generate a resume-worthy project.",
        "Research Topics": "Suggest research ideas."
    }

    st.info(mode_description[ai_mode])

    # -----------------------------
    # Auto Prompt Generator
    # -----------------------------

    auto_prompts = {
        "Video Summary": "Summarize this video.",
        "Explain Simply": "Explain this video in simple language.",
        "Project Ideas": "Suggest projects related to this video.",
        "Interview Questions": "Generate interview questions from this video.",
        "Quiz Generator": "Generate 15 MCQs with answers from this video.",
        "Learning Roadmap": "Create a roadmap to master this topic.",
        "Coding Challenges": "Generate coding challenges based on this topic.",
        "Resume Project Builder": "Create a resume-worthy project based on this video.",
        "Research Topics": "Suggest research topics based on this video."
    }

    # -----------------------------
    # Display previous messages
    # -----------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # -----------------------------
    # Auto Generate Button
    # -----------------------------

    auto_prompt = None

    if ai_mode != "Ask Questions":

        if st.button(f"Generate {ai_mode}", use_container_width=True):
            auto_prompt = auto_prompts[ai_mode]

    # -----------------------------
    # Manual Chat Input
    # -----------------------------

    prompt = st.chat_input("Ask anything about this video...")

    if auto_prompt:
        prompt = auto_prompt

    # -----------------------------
    # Generate Response
    # -----------------------------

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Search Vector DB
        results = rag.search(
            st.session_state.video_id,
            prompt
        )

        context = "\n\n".join(results["documents"][0])

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = chat.generate_answer(
                    context=context,
                    question=prompt,
                    mode=ai_mode
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

# ==============================
