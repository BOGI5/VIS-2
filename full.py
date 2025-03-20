from flask import Flask, send_file, Response, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
import threading
import time

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

if __name__ == '__main__':
    # Start the call in a separate thread
    threading.Thread(target=make_call).start()
    
    # Run the Flask server
    app.run(port=5000)
