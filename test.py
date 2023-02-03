import requests
import json
resp = requests.post("http://127.0.0.1:8080/predict", json={'text': 'I want to innovate an existing technology company to make it better'})
print(resp.json())