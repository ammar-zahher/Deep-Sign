import moviepy as mp
import google.generativeai as genai
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import os

genai.configure(api_key="Add your API key")


def extract_audio_and_transcribe(video_path):
    try:
        print("--- Extracting audio from video... ---")
        video_path = input("Please enter your video path:")
        video_path = video_path.strip()
        video = mp.VideoFileClip(video_path)
        audio_path = "temp_audio.mp3"
        video.audio.write_audiofile(audio_path)
        print("-----Analysis underway.....-----")
        sample_file = genai.upload_file(path=audio_path)
        model = genai.GenerativeModel("models/gemini-3.1-flash-lite")
        response = model.generate_content(
            [
                sample_file,
                "Extract text from this audio clip with high accuracy. "
                "It is forbidden to write any introductions or conclusions. "
                "I want the extracted text only as it is heard."
                "Avoid unnecessary filler words to ensure they can be easily translated into sign language later.",
            ]
        )
        print("\n--- Extracted text : ---")
        raw_text = response.text
        reshaped_text = reshape(raw_text)
        final_text = get_display(reshaped_text)
        print("\n--- Extracted text : ---")
        print(final_text)
        return final_text
    except Exception as e:
        print(f"An error occurred: {e}")


extract_audio_and_transcribe("video_test.mp4")
