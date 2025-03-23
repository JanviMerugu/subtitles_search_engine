import os
import wave
import vosk
import json
import subprocess

def convert_mp3_to_wav(mp3_path, wav_path):
    """ Converts an MP3 file to WAV format using FFmpeg """
    print(f"🔄 Converting {mp3_path} to {wav_path}...")
    
    try:
        subprocess.run(
            ["ffmpeg", "-i", mp3_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path], 
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"✅ Conversion complete: {wav_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in conversion: {e}")
        return None

def transcribe_audio(audio_file):
    """ Transcribes audio using Vosk ASR """

    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return
    
    wf = wave.open(audio_file, "rb")

    # Ensure Vosk model exists
    model_path = "vosk_model"
    if not os.path.exists(model_path):
        print(f"❌ Model not found at {model_path}")
        return
    
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

    print("🔍 Transcribing audio...")
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)

    result = json.loads(recognizer.FinalResult())
    print("📝 Transcription:", result.get("text", "No transcription available."))

# Define file paths
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
audio_mp3 = os.path.join(script_dir, "some_audio.mp3")   # Input MP3 file
audio_wav = os.path.join(script_dir, "some_audio.wav")   # Converted WAV file

# Convert and Transcribe
convert_mp3_to_wav(audio_mp3, audio_wav)
transcribe_audio(audio_wav)
