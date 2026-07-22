import streamlit as st
import core.extractor
from core.extractor import VideoExtractor
from core.transcriber import Transcriber
from core.rag_engine import RAGEngine
from core.chat_engine import ChatEngine


st.write("Extractor file:", core.extractor.__file__)
st.write("Has get_transcript:", hasattr(VideoExtractor, "get_transcript"))

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="InsightTube AI",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 InsightTube AI")
st.caption("AI-Powered Video Intelligence Platform")

# ==========================================
# CACHE EXPENSIVE OBJECTS
# ==========================================

@st.cache_resource
def get_extractor():
    return VideoExtractor()


@st.cache_resource
def get_transcriber():
    return Transcriber()


@st.cache_resource
def get_rag():
    return RAGEngine()


@st.cache_resource
def get_chat():
    return ChatEngine()


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "video": None,
    "video_id": None,
    "transcript": None,
    "segments": None,
    "messages": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# SIDEBAR
# ==========================================

page = st.sidebar.radio(
    "Navigation",
    ["Analyze Video", "AI Chat"],
    label_visibility="collapsed",
)

# ==========================================
# ANALYZE VIDEO
# ==========================================

if page == "Analyze Video":

    st.subheader("Analyze YouTube Video")

    url = st.text_input(
        "Paste YouTube URL",
        placeholder="https://youtube.com/watch?v=..."
    )

    if st.button("Analyze Video", use_container_width=True):

        if not url.strip():
            st.warning("Please enter a YouTube URL.")
            st.stop()

        extractor = VideoExtractor()

        st.write(type(extractor))
        st.write(hasattr(extractor, "get_transcript"))

        try:

            # ------------------------------------
            # STEP 1
            # ------------------------------------

            with st.spinner("Fetching video information..."):
                video = extractor.get_info(url)

            # ------------------------------------
            # STEP 2
            # ------------------------------------

            transcript_data = None

            with st.spinner("Checking YouTube captions..."):
                transcript_data = extractor.get_transcript(
                    video["id"]
                )

            # ------------------------------------
            # STEP 3
            # ------------------------------------

            if transcript_data:

                st.success("Official YouTube transcript found.")

            else:

                st.info(
                    "Transcript unavailable.\n\nUsing Whisper AI..."
                )

                with st.spinner("Downloading audio..."):
                    audio_path = extractor.download_audio(url)

                with st.spinner("Transcribing audio..."):
                    transcriber = get_transcriber()

                    transcript_data = transcriber.transcribe(
                        audio_path
                    )

            # ------------------------------------
            # STEP 4
            # ------------------------------------

            with st.spinner("Building AI knowledge base..."):

                rag = get_rag()

                rag.index_video(
                    video_id=video["id"],
                    transcript=transcript_data["transcript"]
                )

            # ------------------------------------
            # SAVE
            # ------------------------------------

            st.session_state.video = video
            st.session_state.video_id = video["id"]
            st.session_state.transcript = transcript_data["transcript"]
            st.session_state.segments = transcript_data["segments"]
            st.session_state.messages = []

            st.success("Video processed successfully!")

        except Exception as e:

            st.error(f"❌ {e}")

    # ------------------------------------
    # SHOW RESULTS
    # ------------------------------------

    if st.session_state.video:

        video = st.session_state.video

        st.image(video["thumbnail"], use_container_width=True)

        st.subheader(video["title"])

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Channel:**", video["channel"])
            st.write("**Duration:**", video["duration"], "seconds")

        with col2:

            st.write(
                "**Views:**",
                f"{video['view_count']:,}"
                if video["view_count"] else "N/A"
            )

            st.write(
                "**Upload Date:**",
                video["upload_date"]
            )

        with st.expander("Transcript"):

            st.write(st.session_state.transcript)

# ==========================================
# AI CHAT
# ==========================================

else:

    st.subheader("💬 Chat with Video")

    if st.session_state.video is None:

        st.warning("Analyze a video first.")
        st.stop()

    rag = get_rag()
    chat = get_chat()

    ai_mode = st.selectbox(

        "Learning Mode",

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

            "Research Topics",

        ]

    )

    descriptions = {

        "Ask Questions":
            "Ask anything from the video.",

        "Video Summary":
            "Generate a concise summary.",

        "Explain Simply":
            "Explain for beginners.",

        "Project Ideas":
            "Generate practical projects.",

        "Interview Questions":
            "Interview preparation.",

        "Quiz Generator":
            "Generate MCQs.",

        "Learning Roadmap":
            "Learning roadmap.",

        "Coding Challenges":
            "Practice coding.",

        "Resume Project Builder":
            "Resume-ready projects.",

        "Research Topics":
            "Generate research ideas."

    }

    st.info(descriptions[ai_mode])

    auto_prompts = {

        "Video Summary":
            "Summarize this video.",

        "Explain Simply":
            "Explain this video simply.",

        "Project Ideas":
            "Suggest projects from this video.",

        "Interview Questions":
            "Generate interview questions.",

        "Quiz Generator":
            "Generate 15 MCQs with answers.",

        "Learning Roadmap":
            "Create a learning roadmap.",

        "Coding Challenges":
            "Generate coding challenges.",

        "Resume Project Builder":
            "Create a resume-worthy project.",

        "Research Topics":
            "Generate research ideas."

    }

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    auto_prompt = None

    if ai_mode != "Ask Questions":

        if st.button(
            f"Generate {ai_mode}",
            use_container_width=True
        ):

            auto_prompt = auto_prompts[ai_mode]

    prompt = st.chat_input(
        "Ask anything about this video..."
    )

    if auto_prompt:

        prompt = auto_prompt

    if prompt:

        st.session_state.messages.append(

            {

                "role": "user",

                "content": prompt

            }

        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                results = rag.search(

                    st.session_state.video_id,

                    prompt

                )

                documents = results.get("documents", [[]])

                context = "\n\n".join(
                    documents[0]
                ) if documents else ""

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