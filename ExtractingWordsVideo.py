import speech_recognition as sr
import re
import nltk
from nltk.corpus import stopwords
# ffmpeg -i /Users/mananmehra/Downloads/interviw.webm -vn -acodec pcm_s16le -ar 44100 -ac 2 /Users/mananmehra/Downloads/output_audio.wav

question1=[
    "Name",
    "Location",
    "Academic Background",
    "Work Experience",
    "Job Roles",
    "Responsibilities",
    "Achievements",
    "Technical Skills",
    "Soft Skills",
    "Certifications",
    "Degrees",
    "Institutions",
    "Aspirations",
    "Job Expectations",
    "Company Interest",
    "Industry Interest",
    "Alignment with Skills"
]

question2=[
    "Communication",
    "Leadership",
    "Teamwork",
    "Problem solving",
    "Adaptability",
    "Time management",
    "HTML",
    "CSS",
    "Javascript",
    "React",
    "Docker",
    "Node.js",
    "Express.js",
    "postman",
    "mongoDB",
    "MySQL",
    "Python",
    "C++",
    "C#",
    "DSA"
]


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

def extract_keywords_from_text(text):
    words = nltk.word_tokenize(text.lower())

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    words = [word for word in words if re.match(r'^[a-zA-Z]+$', word)]

    return words

def calculate_percentage_of_matches_ques1(extracted_words, dataset):
    match_count = sum(1 for word in extracted_words if word in dataset)
    percentage = (match_count / len(question1)) * 100
    return percentage

def calculate_percentage_of_matches_ques2(extracted_words, dataset):
    match_count = sum(1 for word in extracted_words if word in dataset)
    percentage = (match_count / len(question2)) * 100
    return percentage
# Provide the correct audio file path (generated using ffmpeg)

audio_path_Ques1 = '/Users/mananmehra/Desktop/HR Optiflow/audio_videos/output_audio_Ques1.wav'
audio_path_Ques2 = '/Users/mananmehra/Desktop/HR Optiflow/audio_videos/output_audio_Ques2.wav'
# result1 = extract_words_from_audio(audio_path_Ques1)
# result2 = extract_words_from_audio(audio_path_Ques2)
# if result1:
#     print("Extracted Words for Question 1:", result1)
# if result2:
#     print("Extracted Words for Question 2:",result2)
# keywords_result1 = extract_keywords_from_text(result1)
# keywords_result2 = extract_keywords_from_text(result2)
# print("Keywords for Question 1:", keywords_result1)
# print("Keywords for Question 2:", keywords_result2)

# percentage_Ques1=calculate_percentage_of_matches_ques1(keywords_result1,question1)
# percentage_Ques2=calculate_percentage_of_matches_ques2(keywords_result2,question2)

# print(percentage_Ques1)
# print(percentage_Ques2)
