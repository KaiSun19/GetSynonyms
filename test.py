import requests
import json
#resp = requests.post("http://127.0.0.1:8080/predict", json={'text': 'I want to write a fiction story about a depressed artist who goes on a journey of self discovery'})
resp = requests.post("http://127.0.0.1:8080/prompts", json={'text': 'I want to solve global warming by using predictions of artificial intelligence'})
print(resp.json())