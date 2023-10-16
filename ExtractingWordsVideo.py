import speech_recognition as sr

def extract_words_from_audio(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        # Record the audio from the audio file
        audio = recognizer.record(source)

    try:
        # Use Google Web Speech API to recognize speech
        words = recognizer.recognize_google(audio)
        return words
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None

# Provide the correct audio file path (generated using ffmpeg)
audio_path = '/Users/mananmehra/Downloads/output2.wav'  # Replace with the actual path to your converted audio file
result = extract_words_from_audio(audio_path)

if result:
    print("Extracted Words:", result)
