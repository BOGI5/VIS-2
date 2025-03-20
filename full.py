from flask import Flask, send_file, Response, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
import threading
import time
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Load environment variables from .env file
load_dotenv("./api.env")

# Debug: Print the API key to verify it's being loaded
api_key = os.getenv("ELEVENLABS_API_KEY")
print("API Key:", api_key)

if not api_key:
    raise ValueError("ELEVENLABS_API_KEY is not set in the .env file.")

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)

# Your Twilio credentials
account_sid = 'ACddbb6ca1be8a36d8e4d5131d140758a8'
auth_token = 'a5bb20787212ec76d4a8706379f2c56d'
client = Client(account_sid, auth_token)

# Path to your pre-recorded MP3 file
AUDIO_FILE = 'VIS2.mp3'  # Replace with your actual file name

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
    
    # Play the pre-recorded audio
    response.play(url='https://a292-194-141-252-114.ngrok-free.app/audio')  # Update with your ngrok URL
    
    # Record the recipient's response for 10 seconds
    response.record(
        max_length=20,
        action='/handle-recording',  # URL to handle the recording result
        recording_status_callback='/recording-status'  # (Optional) Handle recording status
    )
    
    return Response(str(response), mimetype='text/xml')

# Route to handle recording result
@app.route('/handle-recording', methods=['POST'])
def handle_recording():
    """Handle the recording result."""
    recording_url = request.form.get("RecordingUrl")
    
    if recording_url:
        print(f"Recording URL: {recording_url}")
        
        # Optionally, you can save the recording URL to a file or database
        with open("recordings.txt", "a") as f:
            f.write(f"{recording_url}\n")
    
    # End the call
    response = VoiceResponse()
    response.hangup()
    
    return Response(str(response), mimetype='text/xml')

def make_call():
    """Make a call using Twilio, play the pre-recorded audio, and record the response."""
    time.sleep(2)  # Give Flask server some time to start
    try:
        call = client.calls.create(
            to='+359895526377',  # Replace with the recipient's phone number
            from_='+12243318146',  # Your Twilio number
            url='https://a292-194-141-252-114.ngrok-free.app/initial',  # URL to start the call flow
            record=True  # Enable recording
        )
        print(f"Call initiated successfully. Call SID: {call.sid}")
    except Exception as e:
        print(f"Failed to initiate call: {e}")

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    # Get the text from the POST request body
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = data["text"]

    try:
        # Convert text to audio
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        print("Audio generated successfully.")
    except Exception as e:
        print("Error generating audio:", e)
        return jsonify({"error": str(e)}), 500

    # Save the audio to a file
    output_file = "./output.mp3"  # Name of the output file

    # Ensure the file is truncated (optional, since 'wb' mode already does this)
    if os.path.exists(output_file):
        os.remove(output_file)  # Delete the file if it exists

    try:
        with open(output_file, "wb") as f:
            # Collect all data from the generator and write it to the file
            for chunk in audio:
                f.write(chunk)
        print(f"Audio saved successfully as {output_file}.")
    except Exception as e:
        print("Error saving audio file:", e)
        return jsonify({"error": str(e)}), 500

    # Play the generated audio (optional)
    try:
        # Reset the generator (if needed) before playing
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        play(audio)
        print("Audio played successfully.")
    except Exception as e:
        print("Error playing audio:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Audio generated and saved successfully", "file": output_file}), 200


if __name__ == '__main__':
    # Start the call in a separate thread
    threading.Thread(target=make_call).start()
    
    # Run the Flask server
    app.run(port=5000)
