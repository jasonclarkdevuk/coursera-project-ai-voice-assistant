from openai import OpenAI
import requests

openai_client = OpenAI()

# Take in audio data received from the browser and pass to IBM Watson STT
# Return the transcription of the audio data
def speech_to_text(audio_binary):
    # Set up Watson SST HTTP API URL
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + "/speech-to-text/api/v1/recognize"

    # Set up parameters for request
    # Use US English model for processing speech
    parameters = {
        "model": "en-US-_Multimedia"
    }

    # Set up request body - sending audio data in body of POSt request
    body = audio_binary

    # Send HTTP POST request
    # Convert response to JSON
    response = requests.post(api_url, params=params, data=audio_binary)

    # Parse response
    text = null
    if response.get("results"):
        latest_result = response.get("results")[-1]
        latest_text = latest_result.get("alternatives")[-1].get("transcript")

        print("Recognised Text: ", latest_text)

        text = latest_text
    
    return text

def text_to_speech(text, voice=""):
    return None


def openai_process_message(user_message):
    return None
