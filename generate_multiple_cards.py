import os
import main
import verb_list
from tqdm import tqdm

lines = verb_list.input.split("\n")[10:]
word_list = """"""
error = ""
for i, line in tqdm(enumerate(lines), total=len(lines)):
    word = line.split("/")[0].strip()
    return_header = i == 0
    try: 
        card = main.generate_anki_card(word, return_header=return_header)
        word_list += card
    except:
        error += f"{word}\n"
        print(f"Can't generate: {word}")

with open(os.path.join(main.CARD_OUTPUT_DIR, "verb_list.txt"), "w", encoding="utf-8") as f:
    f.write(word_list)

with open(os.path.join(main.CARD_OUTPUT_DIR, "error_list.txt"), "w", encoding="utf-8") as f:
    f.write(error)

print("Done!")