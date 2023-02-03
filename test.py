import requests
import json
resp = requests.post("http://127.0.0.1:8080", json={'text': 'I want to create an innovative theory about how people respect eachother'})
print(resp.json())