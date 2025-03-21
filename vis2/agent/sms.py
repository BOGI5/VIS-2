import os
from twilio.rest import Client
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Setup logging
logger = logging.getLogger(__name__)

# Get environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(message: str, to: str):
    """
    Send an SMS message using Twilio.

    Args:
        message: The message to send
        to: The phone number to send the message to
    """
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to,
        )
        logger.info(f"SMS sent to {to} with message: {message.body}")
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
