#!/usr/bin/env python3
import requests
import json

url = "http://localhost:8000/analyze"
data = {"query": "test", "top_k": 1}

try:
    print("Testing /analyze endpoint...")
    response = requests.post(url, json=data, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")