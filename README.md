### Create an Anki Card for German learning

I wanted to create my own [Anki](https://apps.ankiweb.net) deck for learning German. I know there are existing ones out there, but the point was to create something that is relevant for me and that contain the words that I often want/try to use. It was also important for me to have the actual pronuncition of the words.

For this, I've used the audio files available at [Der deutsche Wortschatz](https://www.dwds.de) website. The sample sentences are generated with Gemma 3, downloaded with Ollama. Once a word is generated, I manually upload it to my Deck and sync everything up.

In case one wants to adapt this to their own needs:

### Installation
1) If not already downloaded, get [uv](https://docs.astral.sh/uv/#installation)
2) You also need to install [Ollama](https://ollama.com) and then download the model: `ollama pull gemma3n:e4b`

Once you have that in place: 
```
uv sync
uv run main.py
```

