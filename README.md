# VIS-2 Automated Debt Collection System

## Overview

VIS-2 is an automated debt collection system that uses AI-powered voice calls to contact clients with overdue credit payments. The system combines a web administration panel and an automated calling agent that uses natural language processing to have persuasive conversations with debtors in Bulgarian.

## Key Features

- **Web Administration Panel**: Manage debtor records including personal information and outstanding amounts
- **Automated Voice Calls**: AI-powered voice agent that initiates calls to debtors
- **Natural Language Processing**: Understands and responds to debtor explanations or excuses
- **Voice Synthesis & Recognition**: Uses ElevenLabs for realistic voice generation and speech recognition
- **Conversation Loop**: Maintains a continuous dialogue with debtors until a resolution is reached
- **Aggressive Collection Approach**: Designed to be persistent and persuasive in debt collection

## System Architecture

The system consists of two main components:

1. **Web Administration Panel** (`app.py`)
   - Flask web application for adding, viewing, and managing debtor records
   - SQLite database for user authentication
   - JSON storage for debtor information
   - Triggers the agent calling system

2. **Voice Agent System** (`agent/app.py`)
   - Voice call initiation via Twilio
   - Text-to-speech conversion using ElevenLabs
   - Speech recognition for processing debtor responses
   - Natural language processing via Azure OpenAI
   - Conversation management and response generation

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite, JSON
- **AI/ML Services**:
  - Azure OpenAI for natural language processing
  - ElevenLabs for voice synthesis and speech recognition
- **Telephony**: Twilio for call handling
- **Frontend**: HTML, Bootstrap, JavaScript

## Prerequisites

- Python 3.8+ with Conda environment
- Azure OpenAI API account
- ElevenLabs API account
- Twilio account
- Public URL endpoint (ngrok or similar for development)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/vis2.git
cd vis2
```

### 2. Create Conda Environment

```bash
conda create -n vis2 python=3.8
conda activate vis2
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install azure-ai-inference elevenlabs twilio python-dotenv flask
```

### 4. Environment Configuration

Create a `.env` file in the `agent` directory with the following variables:

```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID=your_elevenlabs_voice_id
MODEL_ID=eleven_multilingual_v2
OUTPUT_FORMAT=mp3
TO=recipient_phone_number
FROM_=your_twilio_phone_number
URL=your_public_url_endpoint
```

You can use the `env_example.txt` file as a template.

### 5. Database Initialization

The SQLite database will be automatically initialized when running the application for the first time. Default credentials:
- Username: `admin`
- Password: `admin123`

### 6. Public URL Setup

To receive calls via Twilio, you need a public URL. For development, you can use ngrok:

```bash
ngrok http 8888
```

Update the `URL` in your `.env` file with the ngrok URL.

## Running the Application

### 1. Start the Web Application

```bash
cd vis2
python app.py
```

The web application will be available at `http://localhost:5000`.

### 2. Using the System

1. **Log in** to the web administration panel using the default credentials
2. **Add a debtor** record with the required information
3. The system will automatically **initiate a call** to the debtor
4. The voice agent will conduct a conversation with the debtor following the instructions in `instructions.txt`

## Agent Behavior Configuration

The agent's behavior is defined in `agent/instructions.txt`. You can modify this file to change how the agent interacts with debtors. The current configuration makes the agent:

- Introduce itself as Vasil Iliev from VIS-2
- Be persistent about collecting the debt
- Explain the current credit situation and consequences of non-payment
- Offer payment options
- Respond aggressively to aggressive clients

## Customization

- **Voice Selection**: Change the `VOICE_ID` in the `.env` file to use a different voice from ElevenLabs
- **Agent Personality**: Modify `instructions.txt` to change the agent's approach and tone
- **Introduction Message**: Edit `introduction.txt` to change the initial greeting

## Security Considerations

This system contains sensitive debtor information and should be deployed with appropriate security measures:

- Use HTTPS for all communications
- Implement proper authentication for the web panel
- Store API keys securely
- Encrypt sensitive data
- Comply with local laws regarding debt collection and recording calls

## Legal Considerations

Before deploying this system:

- Ensure compliance with local debt collection laws and regulations
- Verify compliance with privacy regulations (GDPR, CCPA, etc.)
- Consider legal requirements around call recording and disclosure
- Review terms of service for all third-party APIs used

## Troubleshooting

- **Call not connecting**: Verify Twilio credentials and check that your public URL is accessible
- **Voice synthesis issues**: Check ElevenLabs API key and voice ID
- **Agent not responding properly**: Review Azure OpenAI configuration and ensure the model is available
- **Database errors**: Check file permissions for SQLite database

## License

[Include appropriate license information]

## Disclaimer

This system is designed for legitimate debt collection activities. Use responsibly and in accordance with all applicable laws and regulations.
