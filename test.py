import requests
import json
#resp = requests.post("http://127.0.0.1:8080/predict", json={'text': 'I want to write a fiction story about a depressed artist who goes on a journey of self discovery'})
resp = requests.post("https://getsynonyms-m3jn7lm4ka-uc.a.run.app/prompts", json={'text': 'I want to find a new style of clothes fashion that will be trending in the near future'})
print(resp.json())