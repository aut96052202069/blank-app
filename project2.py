import streamlit as st
import whisper
import asyncio
import websockets
import base64
import openai
# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize Whisper model
model = whisper.load_model("base") # Choose a model size: "base", "small", "medium", or "large"

# Streamlit app setup
st.title("Real-Time Meeting Transcription")

# Create a text area to display the transcription
transcript_area = st.empty()

# WebSocket connection
async def transcribe_meeting(websocket, path):
  async for message in websocket:
    audio_data = message
    try:
      # Transcribe audio data using Whisper
      result = model.transcribe(audio_data)
      text = result["text"]

      # Update the transcript area in Streamlit
      transcript_area.text(text)

    except Exception as e:
      print(f"Error during transcription: {e}")
      transcript_area.text(f"Error: {e}")

async def main():
  # Start the WebSocket server in a separate thread
  server_thread = asyncio.create_task(websockets.serve(transcribe_meeting, "localhost", 8765))

  # Create a Streamlit button to start/stop transcription
  start_button = st.button("Start Transcription")
  if start_button:
    # Wait for the server to start
    await server_thread

    # Display a message and a "Stop" button
    st.success("Transcription started.")
    stop_button = st.button("Stop Transcription")
    if stop_button:
      # Stop the WebSocket server
      await server_thread.cancel()
      st.warning("Transcription stopped.")

if __name__ == "_main_":
  asyncio.run(main())