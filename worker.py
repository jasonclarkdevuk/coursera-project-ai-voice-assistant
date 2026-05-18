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

# Take in prompt and pass to OpenAI's GPT-3 API for a response
def openai_process_message(user_message):
    # Set up prompt for OpenAI API
    prompt = prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations. Keep responses concise - 2 to 3 sentences maximum."

    # Call the OpenAI Api to process our prompt using OpenAI library
    openai_response = openai_client.chat.completions.create(
        model="gpt-5-nano", # Specify the model for processing
        messages=[
            {"role": "system", "content": prompt}, # Set system role and behaviour
            {"role": "user", "content": user_message} # Set user prompt / query
        ],
        max_completion_tokens=1000 # Max number of tokens that can be produced in a reply
    )

    print("OpenAI Response: ", openai_response)

    # Parse and get response message
    response_text = openai_response.choices[0].message.content

    return response_text