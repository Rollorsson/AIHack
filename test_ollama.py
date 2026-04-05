#!/usr/bin/env python3
import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

try:
    print("Testing Ollama connection...")
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": "Say hello in one word",
            "stream": False
        },
        timeout=10
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data.get('response', 'No response')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")