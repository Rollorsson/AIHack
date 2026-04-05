#!/usr/bin/env python3
import requests

url = "http://localhost:8000/search"
data = {"query": "test", "top_k": 1}

try:
    print("Testing /search endpoint...")
    response = requests.post(url, json=data, timeout=60)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")