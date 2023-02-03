from flask import Flask, jsonify, request
import yake
import pickle

model = pickle.load(open('word_embed_model.pkl', 'rb'))

def convert_to_uni(phrase):
  if ' ' in phrase:
    return phrase.split()
  else:
    return phrase

def flatten_list(array):
  flattened_list = []
  for x in array:
    if type(x) == list:
      for y in x:
        flattened_list.append(y)
    else:
      flattened_list.append(x)
  return list(set(flattened_list))


def get_initial_query_keywords(text):
  keyword_model = yake.KeywordExtractor(dedupLim=1)
  keywords = keyword_model.extract_keywords(text)
  uni_keywords = []
  for phrase in keywords:
    uni_keywords.append(convert_to_uni(phrase[1]))
  uni_keywords = flatten_list(uni_keywords)
  return uni_keywords

def add_synonyms(word_list,limit):
  #to already add some displacement we could retrieve word further down the rank 
  all_synonyms = []
  for word in word_list:
    synonyms = []
    top_10 = model.most_similar(word)
    for x in range(limit):
      synonyms.append(top_10[x][0])
    all_synonyms.append(synonyms)
    all_synonyms.append(word)
  all_synonyms.append(word_list)
  return flatten_list(all_synonyms)

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            text = request.json['text']
            tokens = get_initial_query_keywords(text)
            prediction = add_synonyms(tokens,2)
            data = {'synonyms' : prediction}
            return data
        except TypeError as e:
            result = jsonify({'error': str(e)})
    return 'OK'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)