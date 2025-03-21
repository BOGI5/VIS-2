import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional
import time

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Setup logging
logger = logging.getLogger(__name__)

# Get environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")


def create_openai_client():
    """
    Create and configure an Azure OpenAI client.

    Returns:
        ChatCompletionsClient: Configured client or None if configuration is invalid
    """
    # Check for Azure OpenAI credentials
    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT]):
        logger.error(
            "Missing Azure OpenAI credentials - check environment variables")
        return None

    # Initialize OpenAI client
    try:
        logger.info(
            f"Initializing Azure OpenAI client with endpoint: {AZURE_OPENAI_ENDPOINT}")
        client = ChatCompletionsClient(
            endpoint=AZURE_OPENAI_ENDPOINT,
            credential=AzureKeyCredential(AZURE_OPENAI_API_KEY),
        )
        return client
    except Exception as e:
        logger.error(f"Error initializing Azure OpenAI client: {str(e)}")
        return None


def get_completion_with_retries(
    text: str,
    system_prompt: str,
    max_retries: int = 3,
    retry_delay: int = 60,
    temperature: float = 0
) -> Dict[str, Any]:
    """
    Call Azure OpenAI with retry logic.

    Args:
        text: The text to send to the model
        system_prompt: Instructions for the model
        max_retries: Maximum number of retry attempts
        retry_delay: Base delay between retries in seconds
        temperature: Model temperature setting
        response_format: Optional format for the response

    Returns:
        Dict containing the response or error information
    """
    client = create_openai_client()
    if not client:
        return {"error": "Azure OpenAI credentials not configured"}

    # Using exponential backoff for retries
    for attempt in range(max_retries):
        try:
            logger.info(f"API call attempt {attempt+1}/{max_retries}")

            messages = [
                SystemMessage(content=system_prompt),
                UserMessage(content=text)
            ]

            start_time = time.time()
            response = client.complete(
                messages=messages,
                temperature=temperature
            )
            end_time = time.time()

            # Parse the response
            response_text = response.choices[0].message.content

            result = {"content": response_text}

            # Add processing time metadata
            result["processing_time"] = f"{end_time - start_time:.2f} seconds"

            logger.info("API call completed successfully")
            logger.info("Processing time: " + result["processing_time"])

            return result

        except Exception as api_error:
            logger.error(
                f"Error in API call (attempt {attempt+1}): {str(api_error)}")
            if attempt < max_retries - 1:
                backoff_time = retry_delay * (2 ** attempt)
                logger.info(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)  # Exponential backoff

    logger.error(f"All {max_retries} API call attempts failed")
    return {"error": "Failed after multiple attempts"}
