import os

def test_openai_api_key():
    assert 'OPENAI_API_KEY' in os.environ, "OPENAI_API_KEY environment variable not set"
