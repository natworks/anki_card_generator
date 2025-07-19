import os
import helper

MEDIA_OUTPUT_DIR = os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.media")
CARD_OUTPUT_DIR = os.path.expanduser("~/Desktop")


def generate_anki_card(input_word, return_header=True):

    try:
        html = helper.get_website_component(input_word)
        header = html.find("h1", {"class": "dwdswb-ft-lemmaansatz"})
        german_word = header.text
    except:
        print("unable to find word")

    # print("Getting translation, generating sample sentences...")
    example_one, example_two, translation = helper.generate_samples_and_translation(input_word.strip())

    spans = html.find_all("span", {"class": "dwdswb-ft-blocktext"})

    audio_tag = html.find("audio").find("source")
    audio_url = audio_tag["src"]

    sound_file = os.path.basename(audio_url)
    output_file  = os.path.join(MEDIA_OUTPUT_DIR, sound_file)
    if not os.path.exists(output_file):
        helper.download_file(audio_url, output_file)

    word_class = spans[0].text.strip().split("·")[0].strip()

    if "Substantiv" in word_class:
        word_class = "Substantiv"
        class_information = spans[0].text.strip().split("·")[-1].split(":")[-1].strip()
    elif "Verb" == word_class:
        class_information = spans[0].text.strip().split("·")[-1].strip()
    elif "Adjektiv" == word_class:
        class_information = spans[0].text.strip().split("·")[-2:]
        class_information = " ".join(adj.strip() for adj in class_information)
    else:
        pass

    new_card = helper.create_new_card(
        german_word.capitalize(), class_information, sound_file, translation, example_one, example_two, word_class, return_header
    )
    
    return new_card
    

if __name__ == "__main__":

    word = input("Enter a German word: ").strip()
    card = generate_anki_card(word)
    with open(os.path.join(CARD_OUTPUT_DIR, f"{word}.txt"), "w", encoding="utf-8") as f:
        f.write(card)

    print("Done!")