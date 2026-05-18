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
    return None

@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    response = app.response_class(
        response=json.dumps({"openaiResponseText": None, "openaiResponseSpeech": None}),
        status=200,
        mimetype='application/json'
    )
    return response

# Start app
if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
