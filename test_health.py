#!/usr/bin/env python3
import requests

url = "http://localhost:8000/health"

try:
    print("Testing /health endpoint...")
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")