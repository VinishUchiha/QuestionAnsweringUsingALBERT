import torch
import flask
from flask import Flask, request, render_template
import json
import albert.albert_base as albert
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import scipy

app = Flask(__name__)
df = pd.read_csv('data.csv')
embedder = SentenceTransformer('bert-base-nli-mean-tokens')

corpus = df['country'].tolist()
texts = df['economy_overview'].tolist()
corpus_embeddings = embedder.encode(corpus)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        question = request.json['input_question']
        question = question.lstrip().rstrip()
        
        queries = [question]
        query_embeddings = embedder.encode(queries)
        for query, query_embedding in zip(queries, query_embeddings):
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])
            idxx,_ = results[0]
            text = texts[idxx].strip()
            

        # Generate response
        res_albert = albert.answer(question, text)

        res = {'albert': res_albert,
                'text_paragraphs': text}
        return flask.jsonify(res)
    except Exception as error:
        res = str(error)
        return app.response_class(response=json.dumps(res), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, use_reloader=False)
