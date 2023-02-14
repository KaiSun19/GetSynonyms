from flask import Flask, jsonify, request
import yake
import pickle
# import gensim.downloader as api
from flask_cors import CORS
import random
import pandas as pd
import regex as re
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string

model = None
doc2VecModel = None
PromptsDatabase = None

nltk.download("stopwords")

def load_model():
    global model
    model =  pickle.load(open('word_embed_model.pkl', 'rb'))
    print('word embed model loaded')

def load_word2Vec():
  global doc2VecModel
  doc2VecModel = pickle.load(open('doc2Vec.pkl', 'rb'))
  print('doc vec model loaded')


def load_database():
  global PromptsDatabase
  PromptsDatabase = pd.read_json('https://github.com/KaiSun19/MediumStories/blob/master/mediumStories_extract%20(3).json?raw=true')
  print('database loaded')

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

def clean_string(text, stem="None"):
    final_string = ""
    # Make lower
    text = text.lower()
    # Remove line breaks
    text = re.sub(r'\n', '', text)
    # Remove puncuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    # Remove stop words
    text = text.split()
    useless_words = stopwords.words('english')
    useless_words = useless_words + ['hi', 'im']
    text_filtered = [word for word in text if not word in useless_words]
    # Stem or Lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer() 
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    else:
        text_stemmed = text_filtered
    return text_stemmed

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


def get_prompts(keywords,l_bound,u_bound,n_prompts):
  keywords_vector = doc2VecModel.infer_vector(keywords)
  sims_to_keywords = doc2VecModel.dv.most_similar(keywords_vector, topn=100)
  loosely_related_scores = []
  for x in sims_to_keywords:
    if l_bound < x[1] < u_bound:
      loosely_related_scores.append(x)
  random_chosen_scores = []
  while len(random_chosen_scores) < n_prompts:
    random_score = random.choice(loosely_related_scores)
    if random_score not in random_chosen_scores:
      random_chosen_scores.append(random_score)
  prompts = []
  for score in random_chosen_scores:
    prompts.append(PromptsDatabase.iloc[score[0]]['Summarized Text'])
  return prompts

app = Flask(__name__)
CORS(app)

@app.route('/prompts',methods = ['GET','POST'])
def get_predictions():
    if request.method == 'POST':
        try:
            text = request.json['text']
            tokens = get_initial_query_keywords(text)
            keywords = add_synonyms(tokens,2)
            keywords = clean_string(' '.join(keywords))
            print(keywords)
            prompts = get_prompts(keywords,0.4,0.7,2)
            data = {'prompts' : prompts}
            return data
        except Exception as e:
            result = jsonify({'error': str(e)})
            return result
    return 'OK'

# @app.route('/prompts',methods = ['GET','POST'])
# def prompts():
#     if request.method == 'POST':
#         try:
#             keywords = request.json['text']
#             keywords = clean_string(' '.join(keywords))
#             print(keywords)
#             prompts = get_prompts(keywords,0.5,0.6,3)
#             data = {'prompts' : prompts}
#             return data
#         except TypeError as e:
#             result = jsonify({'error': str(e)})
#     return 'OK'

if __name__ == '__main__':
    load_model()
    load_word2Vec()
    load_database()
    app.run(host="0.0.0.0", port=8080)
