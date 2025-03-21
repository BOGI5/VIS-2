from twilio.rest import Client
import os
import time
import requests
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import logging
import json
from agent import get_completion_with_retries

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Setup logging
logger = logging.getLogger(__name__)

# Get environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
MODEL_ID = os.getenv("MODEL_ID")
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
URL=os.getenv("URL")

def generate_audio(text: str, audio_file_name: str):
    """Generate audio from text using ElevenLabs.
    
    Args:
        text (str): The text to convert to audio
        audio_file_name (str): The name of the audio file to save
    """
    try:
        logger.info("The API key is: " + ELEVENLABS_API_KEY)
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
     
        audio = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT,
        )
        
        with open(audio_file_name, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        logger.info(f"Audio generated successfully and saved as {audio_file_name}.")
        
    except Exception as e:
        logger.error(f"Error generating audio: {e}")


def make_call( to: str, from_: str, url: str, timeout: int = 2):
    """Make a call using Twilio and play the generated audio.
    Args:
        timeout (int): The time to wait before making the call (default 2 seconds)
        to (str): The recipient's phone number
        from_ (str): Your Twilio phone number   
        url (str): The URL that forwards to the local server 
    """
    time.sleep(timeout)  # Give the Flask server time to start
    try:
        call = TWILIO_CLIENT.calls.create(
            to=to,  # recipient's phone number
            from_=from_,  # Your Twilio number
            url=url  # Update with your ngrok URL
        )
        print(f"Call initiated successfully. Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to initiate call: {e}")


def download_mp3(url, username, password, output_filename, timeout=2):
    """
    Download an MP3 file from a URL using Basic Authentication
    
    Args:
        url: The URL of the MP3 file
        username: Basic Auth username
        password: Basic Auth password
        output_filename: Name of the file to save the MP3 to
    """
    try:
        # Make the request with basic authentication
        time.sleep(timeout)
        response = requests.get(url, auth=(username, password))
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the content to a file
            with open(output_filename, 'wb') as file:
                file.write(response.content)
            logger.info(f"Successfully downloaded MP3 to {output_filename}")

            
            return True
        else:
            logger.info(f"Failed to download MP3. Status code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error downloading MP3: {str(e)}")
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
        api_key=ELEVENLABS_API_KEY
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
