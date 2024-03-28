import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import datetime

# Get the current timestamp and create a directory
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
os.makedirs(timestamp, exist_ok=True)

# Load the video file
video = mp.VideoFileClip("extract.mp4").subclip(
    6*60-1, 38*60)  # Extract between 5:59 and 38:00 minutes

# Extract audio from the video
audio = video.audio
audio.write_audiofile("extracted_audio.wav")

# Convert to AudioSegment
audio_segment = AudioSegment.from_wav("extracted_audio.wav")

# Split audio into chunks based on silence
chunks = split_on_silence(
    audio_segment,
    # Length of silence to consider a split (in milliseconds)
    min_silence_len=1000,
    silence_thresh=-40  # Silence threshold (in dB)
)

recognizer = sr.Recognizer()

for i, chunk in enumerate(chunks):
    # Export chunk to wav
    chunk_filename = f"{timestamp}/sound_{i+1:04}.wav"
    chunk.export(chunk_filename, format="wav")

    # Use speech_recognition to transcribe the chunk
    with sr.AudioFile(chunk_filename) as source:
        audio_listened = recognizer.record(source)
        try:
            # Recognize the chunk using Google's free API
            text = recognizer.recognize_google(audio_listened)
            print(f"Chunk {i+1}: {text}")
            # Save the transcription to a file
            with open(f"{timestamp}/sound_{i+1:04}.txt", 'w') as f:
                f.write(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
