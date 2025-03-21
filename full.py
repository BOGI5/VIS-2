from flask import Flask, send_file, Response, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
import threading
import time
import requests
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from http.client import HTTPSConnection
from base64 import b64encode

# Load environment variables from .env file
load_dotenv("./api.env")

# Debug: Print the API key to verify it's being loaded
api_key = os.getenv("ELEVENLABS_API_KEY")
print("API Key:", api_key)

if not api_key:
    raise ValueError("ELEVENLABS_API_KEY is not set in the .env file.")

# Initialize Flask app
app = Flask(__name__)

# Your Twilio credentials
account_sid = 'AC97da949d94b620e3b91881de6a1bd525'
auth_token = '1c13b73f42a8ab591833d8ee01bde0a7'
twilio_client = Client(account_sid, auth_token)

# The audio file that will be generated
AUDIO_FILE = 'VIS2.mp3'  


def generate_audio(text):
    """Generate audio from text using ElevenLabs."""
    try:
        elevenlabs_client = ElevenLabs(api_key=api_key)
        
        audio = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        with open(AUDIO_FILE, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"Audio generated successfully and saved as {AUDIO_FILE}.")
        
    except Exception as e:
        print(f"Error generating audio: {e}")


# Route to serve the audio file
@app.route('/audio', methods=['GET', 'POST'])
def serve_audio():
    if os.path.exists(AUDIO_FILE):
        return send_file(AUDIO_FILE, mimetype='audio/mpeg')
    else:
        return "Audio file not found", 404

# Route to handle the initial call flow
@app.route('/initial', methods=['GET', 'POST'])
def initial():
    """Serve the initial TwiML to play audio and start recording."""
    response = VoiceResponse()
    
    # Play the generated audio file
    response.play(url='https://29ef-194-141-252-114.ngrok-free.app/audio')  # Update with your ngrok URL
    
    # Record the recipient's response for 20 seconds
    response.record(
        max_length=20,
        action='/handle-recording',  # URL to handle the recording result
    )
    
    return Response(str(response), mimetype='text/xml')

def download_mp3(url, username, password, output_filename, timeout=2):
    """
    Download an MP3 file from a URL using Basic Authentication
    
    Args:
        url: The URL of the MP3 file
        username: Basic Auth username
        password: Basic Auth password
        output_filename: Name of the file to save the MP3 to
    """
    print("Vliza: " + url)
    try:
        # Make the request with basic authentication
        time.sleep(timeout)
        response = requests.get(url, auth=(username, password))
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the content to a file
            with open(output_filename, 'wb') as file:
                file.write(response.content)
            print(f"Successfully downloaded MP3 to {output_filename}")
            return True
        else:
            print(f"Failed to download MP3. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error downloading MP3: {str(e)}")
        return False


def transcribe_audio(file_path: str, language_code: str = "bul") -> str:
    """
    Transcribe an audio file using ElevenLabs API.

    Args:
        file_path (str): Path to the audio file (e.g., 'recorded.mp3').
        language_code (str): Language code of the audio file. Default is 'bul' (Bulgarian).

    Returns:
        str: Transcribed text from the audio file.
    """
    client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY")
    )

    with open(file_path, "rb") as audio_file:
        transcription = client.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1",
            tag_audio_events=True,
            language_code=language_code,
            diarize=True,
        )

    return transcription.text




# Route to handle recording result
@app.route('/handle-recording', methods=['POST'])
def handle_recording():
    """Handle the recording result."""
    recording_sid = request.form.get("RecordingSid")
    
    if recording_sid:
        print(f"Recording SID: {recording_sid}")
        
        try:
            # Download the recording using the Twilio Client Library
            recording = twilio_client.recordings(recording_sid).fetch()
            recording_url = f"https://api.twilio.com/{recording.uri}.mp3".replace(".json", "")
            print(f"Recording URL: {recording_url}")


            username = account_sid
            password = auth_token

            # Download the recording
            download_mp3(recording_url, username, password, "recorded.mp3")

            #c = HTTPSConnection(f"api.twilio.com/")
            #then connect
            #headers = { 'Authorization' : basic_auth(username, password) }
            #c.request('GET', '/{recording_url}', headers=headers)
            #get the response back
            #response = c.getresponse()
            # at this point you could check the status etc
            # this gets the page text

     #       if response.status_code == 200:
     #           with open('recorded.mp3', 'wb') as f:
     #               f.write(response.data)
     #           print("Recording saved successfully as recorded.mp3.")
     #       else:
     #           print(f"Failed to download the recording. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error saving recording: {e}")

    # End the call
    response = VoiceResponse()
    response.hangup()
    
    return Response(str(response), mimetype='text/xml')


def make_call():
    """Make a call using Twilio and play the generated audio."""
    time.sleep(2)  # Give the Flask server time to start
    try:
        call = twilio_client.calls.create(
            to='+359895526377',  # Replace with the recipient's phone number
            from_='+19133576629',  # Your Twilio number
            url='   https://29ef-194-141-252-114.ngrok-free.app/initial'  # Update with your ngrok URL
        )
        print(f"Call initiated successfully. Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to initiate call: {e}")


if __name__ == '__main__':
    
    # Generate the audio from text
    generate_audio("Здравейте! Чичко Ушев се обажда!")
    # Start the call in a separate thread
    threading.Thread(target=make_call).start()
    
    # Run the Flask server
    app.run(port=8888)
