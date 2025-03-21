from voice_functions import download_mp3, generate_audio, make_call, transcribe_audio, get_completion_with_retries
from flask import Flask, Response, request, send_file
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
from dotenv import load_dotenv
import logging
import json

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Setup logging
logger = logging.getLogger(__name__)

# Get environment variables
AUDIO_FILE = 'current_response.mp3'
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
MODEL_ID = os.getenv("MODEL_ID")
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
TO=os.getenv("TO")
FROM_=os.getenv("FROM_")
URL=os.getenv("URL")


@app.route('/handle-recording', methods=['POST'])
def handle_recording():
    """Handle the recording result and continue the conversation loop."""
    recording_sid = request.form.get("RecordingSid")
    
    if recording_sid:
        logger.info(f"Recording SID: {recording_sid}")
        
        try:
            # Download the recording using the Twilio Client Library
            recording = TWILIO_CLIENT.recordings(recording_sid).fetch()
            recording_url = f"https://api.twilio.com/{recording.uri}.mp3".replace(".json", "")
            logger.info(f"Recording URL: {recording_url}")

            print(recording_url) # Game changer! Do not touch this line!

            username = TWILIO_ACCOUNT_SID
            password = TWILIO_AUTH_TOKEN

            download_mp3(recording_url, username, password, "recorded.mp3")

            user_input = transcribe_audio("recorded.mp3")

            print("User input: ", user_input)

            with open("instructions.txt", "r", encoding="utf8") as file:
                instructions = file.read()

                # Read client data
            with open("info.json", "r", encoding="utf-8") as file:
                client_data = json.load(file)

            # Format client data into a text representation
            client_info = f"""
            Информация за клиента:
            - Име: {client_data['firstName']} {client_data['lastName']}
            - Телефон: {client_data['phone']}
            - Дължима сума: {client_data['amount']} лв.
            - Срок на кредита: {client_data['creditExpire']}
            - Семейно положение: {client_data['familyStatus']}
            - Доход: {client_data['income']} лв.
            - ЕГН: {client_data['egn']}
            - Адрес: {client_data['address']}
            - Възраст: {client_data['age']}
            - Работа: {client_data['job']}
            """

            # Build the system prompt with client information
            system_prompt = instructions + "\n\n" + client_info

            result = get_completion_with_retries(user_input, system_prompt)
            print(result["content"])

            generate_audio(result["content"], "current_response.mp3")


        except Exception as e:
            logger.error(f"Error processing recording: {e}")

    # Create the response to continue the loop
    response = VoiceResponse()
    
    # Play the audio file
    response.play(url=f"{URL}/audio")
    
    # Record again, which will call this same endpoint when done
    response.record(
        max_length=10,
        action='/handle-recording',  # This creates the loop by calling back to this same endpoint
    )

    return Response(str(response), mimetype='text/xml')


@app.route('/initial', methods=['GET', 'POST'])
def initial():
    """Serve the initial TwiML to start the conversation loop."""
    response = VoiceResponse()
    
    # Play the generated audio file
    response.play(url=f"{URL}/audio")
    
    # Record the recipient's response
    response.record(
        max_length=10,
        action='/handle-recording',  # URL to handle the recording result
    )

    return Response(str(response), mimetype='text/xml')

@app.route('/audio', methods=['GET', 'POST'])
def serve_audio():
    """Serve the current audio file."""
    if os.path.exists(AUDIO_FILE):
        return send_file(AUDIO_FILE, mimetype='audio/mpeg')
    else:
        return "Audio file not found", 404

if __name__ == '__main__':
    # Generate the initial audio from text
    with open("introduction.txt", "r", encoding="utf8") as f:
        text = f.read()
    generate_audio(text, "current_response.mp3")

    # Make the initial call
    make_call(TO, FROM_, f"{URL}/initial")
    
    # Run the Flask server
    app.run(port=8888)