import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from ollama import chat

CLASS_INFO = {
    "Substantiv": "Nominativ Plural",
    "Verb": "Flexionen",
    "Adjektiv": ""
}

def generate_samples_and_translation(word_prompt):
    samples = chat(model='gemma3n:e4b', messages=[
    {
        'role': 'user',
        'content': f"Generate two sentences in German using the word {word_prompt}. don't give me any explanations, \
            only the 2 sentences with the translation in parathenses in a single line separated by '---'",
    },
    ])

    translation = chat(model='gemma3n:e4b', messages=[
    {
        'role': 'user',
        'content': f"Give me the english translation for the german word {word_prompt}. The answer should contain only \
            the translation and how/when it's normally used. Note if there are similar words in german. No examples needed. No new lines.",
    },
    ])
    # print(samples.message.content)
    sample_one, sample_two = samples.message.content.split("---")

    return sample_one.strip().capitalize(), sample_two.strip().capitalize(), translation.message.content.strip().capitalize()

def download_file(audio_url, output_file):
    # Download the file
    response = requests.get(audio_url)

    # Save the file
    with open(output_file, "wb") as f:
        f.write(response.content)


def create_new_card(german_word, class_info, sound_file, translation, example_one, example_two, word_class, return_header=True):
    header = '#separator:tab\n#html:true\n#tags column:3\n'
    german_english = f'"<b><span style=""color: rgb(0, 0, 0);"">{german_word}</span><span style=""color: rgb(85, 0, 127);"">&nbsp;</span></b>[sound:{sound_file}]"\t"<b>Übersetzung</b>: {translation}<br><span style=""color: rgb(51, 51, 51); background-color: rgb(255, 255, 255);""><b>{CLASS_INFO[word_class]}:</b>&nbsp;</span>{class_info}<br><b>Beispielsätze:</b><br>{example_one}.<br><br>{example_two}"\tDeutsch-Englisch {word_class}\n'
    english_german = f'{translation}\t{german_word}<br>({class_info})\tEnglisch-Deutsch {word_class}\n'
    if return_header:
        return header + german_english + english_german

    return german_english + english_german

def get_website_component(input_word):
    base_url = "https://www.dwds.de/wb/"
    url = base_url + urllib.parse.quote(input_word)
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch DWDS page for '{input_word}'.")
        return
    
    return BeautifulSoup(response.text, "html.parser")
