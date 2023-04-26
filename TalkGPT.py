import os
import openai
import speech_recognition as sr
import whisper
from TTS.api import TTS

from Audio import AudioFile, playAudioFile
from ChatHistory import ChatHistory

# Filenames
chathistory_filename = "data/chathistory.json"
userprompt_filename = "data/user_prompt.wav"
chatgptresponse_filename = "data/system_response.wav"
system_thinking_filename = "data/system_think.wav"
system_prompt_filename = "data/system_prompt.wav"

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')
assistant_objective = "You are an intelligent, knowledgable assistant and answer as expert. Try to be as precise and short as possible. Always answer in the following form: 1) you answer my prompt 2) you ask me a question."
first_prompt = True

# Load chat history if available
chatHistory = ChatHistory(chathistory_filename)
chatHistory.loadMessages()

if chatHistory.isEmpty():
    chatHistory.logNewMessage("system", assistant_objective)
    print("You are starting a new conversation.")

print("Previous conversation :")
print(chatHistory.getAllMessages())
print()
print()

# initialize the recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Load Speech-To-Text (STT) model
whisper_model = whisper.load_model("base")

# Init Text-To-Speech (TTS) model
model_name = "tts_models/en/ljspeech/tacotron2-DDC_ph"
tts = TTS(model_name)

# Prepare system default speech responses
tts.tts_to_file(text="Let me think about it..", speed=1.5, file_path=system_thinking_filename)
tts.tts_to_file(text="How can I help you?", speed=1.5, file_path=system_prompt_filename)


# Speak text
def speak(txt):
    tts.tts_to_file(text=txt, speed=1.5, file_path=chatgptresponse_filename)
    playAudioFile(chatgptresponse_filename)
    
def listenForPrompt(filename):
    global first_prompt
    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        print("calibrating ambient noise..")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        if first_prompt:
            playAudioFile(system_prompt_filename)
            first_prompt = False
        print("say something..")
        audio = recognizer.listen(source,timeout=8,phrase_time_limit=8)

    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())

def convertSTT(filename):
    playAudioFile(system_thinking_filename)
    return whisper_model.transcribe(userprompt_filename)["text"]


def askChatGPT(prompt):
    chatHistory.logNewMessage("user", prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=chatHistory.getAllMessages()
    ).choices[0].message.content

    chatHistory.logNewMessage("assistant", response)

    return response



# Run main conversation loop
while True:
    # Listen to user prompt, save to audio file
    listenForPrompt(userprompt_filename)

    # Extract text from audiofile
    userprompt = convertSTT(userprompt_filename)
    print("your prompt:", userprompt)

    if userprompt != '':
        # Get response from chatgpt and speak
        chatGPTResponse = askChatGPT(userprompt)
        speak(chatGPTResponse)
