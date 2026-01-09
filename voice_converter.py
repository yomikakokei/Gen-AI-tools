"""
Voice converter AI tool v.1.0

Copyright (c) 2026 Yos Yama

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import queue
import threading
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import azure.cognitiveservices.speech as azure_speech

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"  # 展開したフォルダ名に変更

# Azure configuration
AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_REGION")
if not AZURE_KEY or not AZURE_REGION:
    raise ValueError("Please set AZURE_SPEECH_KEY and AZURE_REGION environment variables.")

# Voice options
VOICE_OPTIONS = {
    "1": {"name": "en-US-JennyNeural", "desc": "Female - American English"},
    "2": {"name": "en-US-GuyNeural", "desc": "Male - American English"},
    "3": {"name": "en-IN-NeerjaNeural", "desc": "Female - Indian English"},
    "4": {"name": "en-IN-PrabhatNeural", "desc": "Male - Indian English"},
    "5": {"name": "en-GB-SoniaNeural", "desc": "Female - British English"},
    "6": {"name": "en-GB-RyanNeural", "desc": "Male - British English"},
    "7": {"name": "en-AU-NatashaNeural", "desc": "Female - Australian English"},
    "8": {"name": "en-AU-WilliamNeural", "desc": "Male - Australian English"},
}

def select_voice():
    print("\nAvailable voice options:")
    for key, value in VOICE_OPTIONS.items():
        print(f"{key}: {value['desc']} ({value['name']})")
    while True:
        choice = input("Select a voice (1-8): ").strip()
        if choice in VOICE_OPTIONS:
            return VOICE_OPTIONS[choice]["name"]
        print("Invalid choice. Please enter a number from 1 to 8.")

# Initialize PyAudio
p = pyaudio.PyAudio()
stream_in = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
stream_out = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

# Initialize Vosk (offline STT)
if not os.path.exists(VOSK_MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at '{VOSK_MODEL_PATH}'. Please download and extract it.")
model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, RATE)

# Initialize Azure TTS
selected_voice = select_voice()
speech_config = azure_speech.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
speech_config.speech_synthesis_voice_name = selected_voice
# audio_config=None にすると result.audio_data が取得可能
synthesizer = azure_speech.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

# Queue for passing recognized text
audio_queue = queue.Queue()

def process_audio():
    """Continuously read microphone and recognize speech with Vosk"""
    print("Listening... Speak into the microphone.")
    while True:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    print(f"You said: {text}")
                    audio_queue.put(text)
        except Exception as e:
            print(f"Audio processing error: {e}")

def synthesize_speech():
    """Take text from queue and synthesize with Azure TTS"""
    while True:
        try:
            text = audio_queue.get()
            if not text:
                continue
            print(f"Synthesizing: {text}")
            result = synthesizer.speak_text_async(text).get()

            if result.reason == azure_speech.ResultReason.SynthesizingAudioCompleted:
                audio_data = result.audio_data
                stream_out.write(audio_data)
            elif result.reason == azure_speech.ResultReason.Canceled:
                cancellation = result.cancellation_details
                print(f"Synthesis canceled: {cancellation.reason} - {cancellation.error_details}")
        except Exception as e:
            print(f"Speech synthesis error: {e}")

# Start threads
audio_thread = threading.Thread(target=process_audio, daemon=True)
speech_thread = threading.Thread(target=synthesize_speech, daemon=True)
audio_thread.start()
speech_thread.start()

print(f"\nReal-time voice conversion started with voice: {selected_voice}")
print("Speak into the microphone. Press Ctrl+C to stop.\n")

try:
    # Keep main thread alive
    while True:
        threading.Event().wait(1)
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()
    p.terminate()
    print("Cleanup completed. Goodbye!")
