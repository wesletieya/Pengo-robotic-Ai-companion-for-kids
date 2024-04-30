import pandas as pd
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

file_path = r"C:\Users\ayabe\vs projects\chatbot_pengo\chatbot_data.txt"
#print(text_data)
csv_path = r"C:\Users\ayabe\vs projects\chatbot_pengo\data.csv"
data=pd.read_csv(csv_path)
#print(data.head())

import csv

# Define input and output file paths
input_file_path = "text_data.txt"
output_file_path = "data.csv"

questions = []
responses = []
with open(file_path, 'r') as file:
    text_data = file.read()

sections = text_data.split("**Question:**")[1:]
for section in sections:
    question, response = section.split("**Response:**")[:2]
    questions.append(question.strip())
    responses.append(response.strip())
with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["question", "response"])  # Write headers
    for question, response in zip(questions, responses):
        writer.writerow([question, response])
data=pd.read_csv(r"C:\Users\ayabe\vs projects\chatbot_pengo\data.csv")

data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x)
data['preprocessed'] = data['question'].replace(to_replace=r'[^\w\s]', value='', regex=True)
data['preprocessed'] = data['preprocessed'].apply(word_tokenize)
stop_words = set(stopwords.words('english'))
data['preprocessed'] = data['preprocessed'].apply(lambda x: [word for word in x if word not in stop_words])

stemmer = PorterStemmer()

def stem_words(words):
    return [stemmer.stem(word) for word in words]

data['preprocessed'] = data['preprocessed'].apply(stem_words)

print(data.head())

data.to_csv('data.csv', index=False)

