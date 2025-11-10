import os
import pytest
import requests
from unittest.mock import patch, Mock
from backend.fish_speech_adapter import FishSpeechAdapter, FISH_SPEECH_API_URL, FISH_SPEECH_API_KEY
from fastapi import HTTPException

class MockResponse:
    def __init__(self, status_code, content, headers=None):
        self.status_code = status_code
        self.content = content
        self._headers = headers if headers is not None else {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

    @property
    def headers(self):
        return self._headers

def test_fish_speech_adapter_initialization():
    adapter = FishSpeechAdapter(api_url="http://mock-fish-speech-api.com/synthesize", api_key="mock_api_key")
    assert adapter.api_url == "http://mock-fish-speech-api.com/synthesize"
    assert adapter.api_key == "mock_api_key"

@patch('requests.post')
def test_synthesize_speech_success(mock_post):
    mock_response_instance = MockResponse(
        status_code=200,
        content=b"mock_audio_data",
        headers={"Content-Type": "audio/wav"}
    )
    mock_post.return_value = mock_response_instance
    adapter = FishSpeechAdapter(api_url="http://mock-fish-speech-api.com/synthesize", api_key="mock_api_key")
    text = "Hello, world!"
    audio_data = adapter.synthesize_speech(text)

    mock_post.assert_called_once_with(
        "http://mock-fish-speech-api.com/synthesize",
        headers={
            "X-API-Key": "mock_api_key",
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "speaker_id": "default",
            "output_format": "wav"
        },
        timeout=30
    )
    assert audio_data == b"mock_audio_data"

@patch('requests.post')
def test_synthesize_speech_http_error(mock_post):
    mock_response_instance = MockResponse(
        status_code=400,
        content=b"error_data",
        headers={"Content-Type": "audio/wav"}
    )
    mock_post.return_value = mock_response_instance
    adapter = FishSpeechAdapter(api_url="http://mock-fish-speech-api.com/synthesize", api_key="mock_api_key")
    text = "Error text"

    with pytest.raises(HTTPException) as exc_info:
        adapter.synthesize_speech(text)
    assert exc_info.value.status_code == 503
    assert "Failed to connect to fish-speech service" in exc_info.value.detail

@patch('requests.post')
def test_synthesize_speech_timeout(mock_post):
    adapter = FishSpeechAdapter(api_url="http://mock-fish-speech-api.com/synthesize", api_key="mock_api_key")
    text = "Timeout text"

    mock_post.side_effect = requests.exceptions.Timeout("Request timed out")


    with pytest.raises(HTTPException) as exc_info:
        adapter.synthesize_speech(text)
    assert exc_info.value.status_code == 504
    assert "Fish-speech API request timed out" in exc_info.value.detail

@patch('requests.post')
def test_synthesize_speech_unexpected_content_type(mock_post):
    mock_response_instance = MockResponse(
        status_code=200,
        content=b"not_audio_data",
        headers={"Content-Type": "application/json"} # Unexpected content type
    )
    mock_post.return_value = mock_response_instance
    adapter = FishSpeechAdapter(api_url="http://mock-fish-speech-api.com/synthesize", api_key="mock_api_key")
    text = "Unexpected content type"

    with pytest.raises(HTTPException) as exc_info:
        adapter.synthesize_speech(text)
    assert exc_info.value.status_code == 500
    assert "Unexpected audio format from fish-speech API" in exc_info.value.detail

@patch('requests.post')
def test_synthesize_speech_general_exception(mock_post):
    mock_post.side_effect = Exception("Some unexpected error")
    mock_response_instance = MockResponse(
        status_code=200,
        content=b"mock_audio_data",
        headers={"Content-Type": "audio/wav"}
    )
    mock_post.return_value = mock_response_instance
    adapter = FishSpeechAdapter(api_url="http://mock-fish-speech-api.com/synthesize", api_key="mock_api_key")
    text = "General error text"

    with pytest.raises(HTTPException) as exc_info:
        adapter.synthesize_speech(text)
    assert exc_info.value.status_code == 500
    assert "An unexpected error occurred" in exc_info.value.detail
