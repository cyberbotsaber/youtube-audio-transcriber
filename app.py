import streamlit as st
import whisper
import yt_dlp
import os

# Function to download audio from YouTube
def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'output.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Streamlit UI
def main():
    st.title("YouTube Audio Transcriber")

    # Input: YouTube URL
    video_url = st.text_input("Enter YouTube Video URL:")

    if video_url:
        st.write(f"Downloading audio from: {video_url}")
        download_audio(video_url)
        st.success("Download Complete!")

        # Input: Output Filename
        filename = st.text_input("Enter the filename to save transcription:")

        if filename:
            st.write("Transcribing audio...")
            transcript = transcribe_audio("output.mp3")
            st.success("Transcription Complete!")

            # Displaying the transcription
            st.text_area("Transcription", transcript)

            # Option to download transcription
            st.download_button("Download Transcription", transcript, file_name=filename)

# Run the app
if __name__ == "__main__":
    main()
