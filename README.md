# TalkGPT
Talk with ChatGPT instead of writing and have a verbal conversation with an intelligent assistant.

## How it works.

This project first uses uses the SpeechRecognition library to listen, and save the users prompt as audio. We then use OpenAIs Whisper library to translate the audio to a text prompt. Finally, we request a response from ChatGPT using the OpenAI API and translate it into high quality speech output using the TTS library.

## How to run TalkGPT
#### 1. Navigate into the repository and create a new environment
```
cd TalkGPT/
python -m venv env
source env/bin/activate
```

#### 2. Save your OpenAI API Key as environment variable
```
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

#### 3. (on MacOS) Install portaudio using homebrew, it is required for the pyaudio library
```
brew update
brew install portaudio
```

#### 4. Make sure pip is upgraded, and then install all dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Now you should be able to run TalkGPT using python
```
python TalkGPT.py
```

#### 6. Start talking

## Notes

The conversation is saved in a json file to allow maintaining a conversation over longer time.
You can manually clear the chathistory.json file, or comment out the .loadMessages() call if desired.

## Limitations
Accurately recognising when the user speaks.
Delays induced by processing speech (STT and TTS).

## Dependencies
```
openai
openai-whisper
SpeechRecognition
TTS
pyaudio
wave
```
