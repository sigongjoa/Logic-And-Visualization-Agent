import requests
import logging
import os
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Configuration for the fish-speech API server
FISH_SPEECH_API_URL = os.getenv("FISH_SPEECH_API_URL", "http://localhost:8003/synthesize")
FISH_SPEECH_API_KEY = os.getenv("FISH_SPEECH_API_KEY", "your_fish_speech_api_key")

class FishSpeechAdapter:
    def __init__(self, api_url: str = FISH_SPEECH_API_URL, api_key: str = FISH_SPEECH_API_KEY):
        self.api_url = api_url
        self.api_key = api_key
        logger.info(f"FishSpeechAdapter initialized with API URL: {self.api_url}")

    def synthesize_speech(self, text: str, speaker_id: str = "default", output_format: str = "wav") -> bytes:
        """
        Synthesizes speech from text using the fish-speech API.

        Args:
            text (str): The text to synthesize.
            speaker_id (str): The ID of the speaker to use for synthesis.
            output_format (str): The desired output audio format (e.g., "wav", "mp3").

        Returns:
            bytes: The audio data in the specified format.

        Raises:
            HTTPException: If the API call fails or returns an error.
        """
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "speaker_id": speaker_id,
            "output_format": output_format
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            if response.headers.get("Content-Type") not in ["audio/wav", "audio/mpeg", "audio/x-wav"]:
                logger.error(f"Unexpected content type from fish-speech API: {response.headers.get('Content-Type')}")
                logger.error(f"All response headers: {response.headers}") # Added for debugging
                raise HTTPException(status_code=500, detail="Unexpected audio format from fish-speech API")

            return response.content

        except requests.exceptions.Timeout:
            logger.error(f"Fish-speech API request timed out after 30 seconds for text: {text[:50]}...")
            raise HTTPException(status_code=504, detail="Fish-speech API request timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling fish-speech API: {e} for text: {text[:50]}...")
            raise HTTPException(status_code=503, detail=f"Failed to connect to fish-speech service: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during speech synthesis: {e}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage (for testing purposes)
    adapter = FishSpeechAdapter()
    test_text = "안녕하세요, 물고기 음성 합성 테스트입니다."
    try:
        audio_data = adapter.synthesize_speech(test_text)
        print(f"Successfully synthesized speech for text: '{test_text[:20]}...' (Length: {len(audio_data)} bytes)")
        # In a real application, you would save this audio_data to a file or stream it.
        # For example, to save to a WAV file:
        # with open("test_output.wav", "wb") as f:
        #     f.write(audio_data)
        # print("Audio saved to test_output.wav")
    except HTTPException as e:
        print(f"Error synthesizing speech: {e.detail}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
