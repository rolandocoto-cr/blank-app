import requests
import streamlit as st
import threading

st.set_page_config(page_title="Cook Islands Māori ASR")

ASR_URL = "https://asr-service-790340752928.us-central1.run.app/transcribe"

# ── Sidebar navigation ──────────────────────────────────────────────────────
st.caption("☰ Use the sidebar (top left) to navigate")
page = st.sidebar.radio("Navigate", ["🎙️ Transcribe", "ℹ️ About"])

# ── About page ───────────────────────────────────────────────────────────────
if page == "ℹ️ About":
    st.title("About the Project")
    st.markdown("This page uses an [Wav2Vec2-XLSR](https://huggingface.co/docs/transformers/en/model_doc/xlsr_wav2vec2) model that transforms an audio recording in Cook Islands Māori into a text transcription of the words in the recording.")
    st.markdown("The model was developed by Rolando Coto-Solano, Sally Akevai Nicholas, and students from Dartmouth College. You can read more about the project here: [Development of Automatic Speech Recognition for the Documentation of Cook Islands Māori](https://aclanthology.org/2022.lrec-1.412).")
    st.write("This is part of a larger project by Sally Akevai Nicholas to document the Cook Islands Māori language.")
    #st.button("← Back to TTS", on_click=go_to_main)


# ── Transcribe page ─────────────────────────────────────────────────────────
else:
    st.title("🎙️ Cook Islands Māori Speech Recognition")
    st.write("Upload an audio file or record directly in your browser. "
             "You'll receive the transcription by email.")

    # ── Email input ──────────────────────────────────────────────────────
    email = st.text_input("Your email address")

    # ── Choose input method ──────────────────────────────────────────────
    tab_upload, tab_record = st.tabs(["📁 Upload a file", "🎤 Record audio"])

    def submit_audio(file_name: str, file_content: bytes, user_email: str):
        """Fire the ASR request in a background thread."""
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

    # ── Tab 1: Upload ────────────────────────────────────────────────────
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

    # ── Tab 2: Record ────────────────────────────────────────────────────
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
