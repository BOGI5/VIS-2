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
