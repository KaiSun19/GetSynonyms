import requests
import json
resp = requests.post("https://getsynonyms-m3jn7lm4ka-uc.a.run.app/predict", json={'text': 'I want to become a better person by self-improvement'})
print(resp.json())