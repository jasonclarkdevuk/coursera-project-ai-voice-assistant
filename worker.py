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
    parameters = {"model": "en-US_Multimedia"}

    # Send HTTP POST request
    response = requests.post(
        api_url, params=parameters, data=audio_binary
    ).json()

    text = "null"

    # Check if 'results' exists and is not empty
    if response.get("results"):
        # Safely grab the last result and its last alternative transcript
        latest_result = response.get("results")[-1]
        text = latest_result.get("alternatives")[-1].get("transcript")
        print("Recognised Text: ", text)

    return text

# Pass text data to IBM Watson TTS to get spoken output
def text_to_speech(text, voice=""):
    # Set up Watson TTS HTTP API URL
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    # If user has specified a voice, add parameter to API url
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    
    # Set headers for request
    headers = {
        "Accept": "audio/wav", # Send audio data in WAV format
        "Content-Type": "application/json" # Format of body of POST request is JSON        
    }

    # Set up request body
    json_data = {
        "text": text
    }

    # Send HTTP POST request   
    # Response is binary audio data in the content of response
    response = requests.post(api_url, headers=headers, json=json_data)

    print("TTS Response: ", response)

    return response.content
    
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
