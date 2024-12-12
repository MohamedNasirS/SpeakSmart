import pyaudio
import wave
from gtts import gTTS
from translate import Translator
import speech_recognition as sr
from langdetect import detect

# Function to record audio and save as WAV
def record_audio(output_filename, duration=10, sample_rate=44100, channels=1, chunk_size=1024):
    """Record audio and save it to a WAV file."""
    audio_format = pyaudio.paInt16
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Recording...")
    frames = []

    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size, exception_on_overflow=False)
        frames.append(data)

    print("Recording complete.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {output_filename}")

# Function to recognize speech from WAV file
def recognize_speech_from_file(filename):
    """Recognize speech from an audio file using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        print("Recognizing speech...")
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Speech not clear. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

# Main Program
if __name__ == "__main__":
    wav_file = "output.wav"
    mp3_file = "speech.mp3"
    record_duration = 5

    # Step 1: Record audio
    record_audio(wav_file, duration=record_duration)

    # Step 2: Recognize speech from the recorded audio
    text = recognize_speech_from_file(wav_file)

    if text:
        # Step 3: Detect the language of the recognized text
        detected_language = detect(text)
        print(f"Detected language: {detected_language}")

        # Step 4: Translate the text
        target_language = input("Which language do you want to translate your saying to (e.g., 'es' for Spanish, 'fr' for French): ")
        translator = Translator(from_lang=detected_language, to_lang=target_language)
        translation = translator.translate(text)
        print(f"Translation: {translation}")

        # Step 5: Convert the translated text to speech
        speech = gTTS(text=translation, lang=target_language, slow=False)
        speech.save(mp3_file)
        print(f"Translated speech saved to {mp3_file}")
