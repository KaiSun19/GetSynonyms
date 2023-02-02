import requests
import json
resp = requests.post("http://127.0.0.1:8080", json={'text': 'I want to write a non-fiction story about a depressed artist'})
print(resp.json())