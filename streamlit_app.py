import requests
import streamlit as st
import threading
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Cook Islands Māori NLP")
ASR_URL = "https://asr-service-790340752928.us-central1.run.app/transcribe"

# ── Top navigation menu ─────────────────────────────────────────────────────
page = option_menu(
    menu_title=None,
    options=["Home", "Transcription", "Voice Generation", "Parsing", "Spell Checking", "Forced Alignment", "About"],
    icons=["house", "mic", "volume-up", "file-earmark-text", "spellcheck", "soundwave", "info-circle"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"font-size": "14px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px",
                     "--hover-color": "#ddd"},
        "nav-link-selected": {"background-color": "#ff4b4b"},
    }
)

# ── Home page ────────────────────────────────────────────────────────────────
if page == "Home":
    st.title("🏠 Kia Orana! Welcome")
    st.write(
        "Welcome to the CIM NLP platform."
        "Use the menu above to navigate between tools."
    )

# ── Transcription page ──────────────────────────────────────────────────────
elif page == "Transcription":
    st.title("🎙️ Cook Islands Māori Speech Recognition")
    st.write("Upload an audio file or record directly in your browser. "
             "You'll receive the transcription by email.")

    email = st.text_input("Your email address")

    tab_upload, tab_record = st.tabs(["📁 Upload a file", "🎤 Record audio"])

    def submit_audio(file_name: str, file_content: bytes, user_email: str):
        def send_request():
            try:
                requests.post(
                    ASR_URL,
                    files={"file": (file_name, file_content, "audio/wav")},
                    data={"email": user_email},
                    timeout=3600,
                )
            except Exception:
                pass

        thread = threading.Thread(target=send_request, daemon=True)
        thread.start()

    with tab_upload:
        uploaded = st.file_uploader("Choose an audio file", type=["wav"])

        if st.button("Transcribe uploaded file", key="btn_upload"):
            if not email:
                st.error("Please enter your email address.")
            elif not uploaded:
                st.error("Please upload a WAV file.")
            else:
                file_content = uploaded.read()
                submit_audio(uploaded.name, file_content, email)
                st.success(
                    "✅ Your file has been submitted! You will receive an email "
                    "when processing begins, and another when your transcription "
                    "is ready."
                )

    with tab_record:
        recording = st.audio_input("Click the microphone to start recording")

        if st.button("Transcribe recording", key="btn_record"):
            if not email:
                st.error("Please enter your email address.")
            elif not recording:
                st.error("Please make a recording first.")
            else:
                file_content = recording.read()
                submit_audio("recording.wav", file_content, email)
                st.success(
                    "✅ Your recording has been submitted! You will receive an "
                    "email when processing begins, and another when your "
                    "transcription is ready."
                )

# ── Voice Generation page ───────────────────────────────────────────────────
elif page == "Voice Generation":
    st.title("🔊 Voice Generation")
    st.write("This feature is coming soon.")

# ── Parsing page ─────────────────────────────────────────────────────────────
elif page == "Parsing":
    st.title("📄 Parsing")
    st.write("This feature is coming soon.")

# ── About page ───────────────────────────────────────────────────────────────
elif page == "About":
    st.title("About the Project")
    st.markdown("The speech recognition (transcription) uses an [Wav2Vec2-XLSR](https://huggingface.co/docs/transformers/en/model_doc/xlsr_wav2vec2) model that transforms an audio recording in Cook Islands Māori into a text transcription of the words in the recording.")
    st.markdown("The model was developed by Rolando Coto-Solano, Sally Akevai Nicholas, and students from Dartmouth College. You can read more about the project here: [Development of Automatic Speech Recognition for the Documentation of Cook Islands Māori](https://aclanthology.org/2022.lrec-1.412).")
    st.write("This is part of a larger project by Sally Akevai Nicholas to document the Cook Islands Māori language.")

# ── Spell Checking page ─────────────────────────────────────────────────────
elif page == "Spell Checking":
    st.title("✏️ Spell Checking")
    st.write("This feature is coming soon.")

# ── Forced Alignment page ───────────────────────────────────────────────────
elif page == "Forced Alignment":
    st.title("🔊 Forced Alignment")
    st.write("This feature is coming soon.")
