import base64
import json
from flask import Flask, render_template, request
from flask_cors import CORS

# Bring in external libraries for GPT-3, SST and TTS
from worker import speech_to_text, text_to_speech, openai_process_message

import os

# Flask app created and CORS policy is used
# Policy is used to allow or prevent web pages from making requests to different domains
# Current it can allow any request (*)
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Main index page and function
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("Processing Speech to Text")
    audio_binary = request.data # Get user's speech from their request

    # Call STT function to transcribe the speech using API
    stt = speech_to_text(audio_binary)

    # Return the response back
    # Create bespoke JSON response 
    response = app.response_class(
        response=json.dumps({"text": stt}), # Create simple JSON using dict using actuall STT data 
        status=200, # Success response
        mimetype="application/json" # Format of response as JSON
    )

    print("Response: ", response)
    print("Response Data: ", response.data)

    return response

@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    # Get user's message from request
    user_message = request.json["userMessage"]

    print("User Message: ", user_message)

    # Get preferred voice from request
    voice = request.json["voice"]

    print("Voice: ", voice)

    # Call OpenAI processing with user's prompt and get a response
    openai_response_text = openai_process_message(user_message)

    # Clean response to remove empty lines
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])

    # Call TTS function to convert response to speech
    openai_response_speech = text_to_speech(openai_response_text, voice)

    # Convert to Base64 string so it can be sent back in JSON response
    # Convert binary data to a textual representation by encoding in base64
    openai_response_speech = base64.b64encode(openai_response_speech).decode("utf-8")

    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )

    print("Process Prompt Response: ", response)
    
    return response

# Start app
if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
