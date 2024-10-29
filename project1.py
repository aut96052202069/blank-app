import streamlit as st
import openai
import tempfile
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time

# Set your OpenAI API key here
openai.api_key = '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'

# Streamlit app setup
st.title("Real-Time Transcription for Online Meetings")
st.write("Record audio and get real-time transcription.")

# Record settings
duration = st.slider("Select recording duration (seconds)", min_value=1, max_value=10, value=5)
sample_rate = 44100  # Sample rate for audio recording

# Record audio button
if st.button("Start Recording"):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    st.write("Recording complete!")

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        write(temp_audio_file.name, sample_rate, audio_data)

        # Display the recorded audio
        st.audio(temp_audio_file.name)

        # Transcribe with Whisper API
        st.write("Transcribing audio...")
        try:
            with open(temp_audio_file.name, "rb") as audio_file:
                transcription = openai.Audio.transcribe("whisper-1", audio_file)
                st.write("Transcription:")
                st.write(transcription["text"])
        except Exception as e:
            st.write("Error transcribing audio:", e)