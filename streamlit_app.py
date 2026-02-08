import requests
import streamlit as st
import threading

ASR_URL = "https://asr-service-790340752928.us-central1.run.app/transcribe"

# ── Sidebar navigation ──────────────────────────────────────────────────────
st.caption("☰ Use the sidebar (top left) to navigate")
page = st.sidebar.radio("Navigate", ["🎙️ Transcribe", "ℹ️ About"])

# ── About page ───────────────────────────────────────────────────────────────
if page == "ℹ️ About":
    st.title("About")
    st.write("This project was done by Ake.")

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
