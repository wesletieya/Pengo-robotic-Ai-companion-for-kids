import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import nltk
'''nltk.download('punkt')
nltk.download('stopwords')'''


# Load the dataset
data = pd.read_csv("data.csv")

def preprocess(kid_input):
    kid_input = kid_input.lower()
    kid_input = re.sub(r'[^\w\s]', '', kid_input)
    tokens = word_tokenize(kid_input)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return tokens

def jaccard_similarity(list1, list2):
    intersection = len(set(list1).intersection(list2))
    union = len(set(list1).union(list2))
    return intersection / union

data['preprocessed'] = data['question'].apply(preprocess)

def find_best_match(kid_input, dataset):
    input_preprocessed = preprocess(kid_input)
    similarities = dataset['preprocessed'].apply(lambda x: jaccard_similarity(x, input_preprocessed))
    best_match_index = similarities.idxmax()
    return dataset.iloc[best_match_index]

VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']
VOICE = VOICES[1]

async def generate_speech(text, output_file):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def text_to_speech(response_text):
    output_file = "response.mp3"
    asyncio.run(generate_speech(response_text, output_file))
    audio = AudioSegment.from_mp3(output_file)
    play(audio)

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Pengo: I'm listening...")
        audio = recognizer.listen(source)

    try:
        transcript = recognizer.recognize_google(audio)
        print(f"Child: {transcript}")
    except sr.RequestError:
        print("API was unreachable or unresponsive.")
        return None
    except sr.UnknownValueError:
        a="I couldn't hear you. can you repeat please ?"
        print(a)
        text_to_speech(a)
        return None

    return transcript

# Initialize the recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

start = "Hello kiddo! It's Pengo. Let the adventure of the day begin! "
print("Pengo: "+ start)
text_to_speech(start)

while True:
    input_question = recognize_speech_from_mic(recognizer, microphone)
    if input_question is None:
        continue
    if any(word in input_question.lower() for word in ['quit', 'goodbye', 'exit', 'bye']):
        end = "Pengo: Goodbye!"
        print(end)
        text_to_speech("Goodbye!")
        break
    best_match = find_best_match(input_question, data)
    response = best_match['response']
    print("Pengo: ", response)
    text_to_speech(response)
