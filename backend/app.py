from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import training_date
import threading

from flask_cors import CORS
app = Flask(__name__)
CORS(app)  

app = Flask(__name__)

data = training_date.training_data
texts = [item[0] for item in data]
labels = [item[1] for item in data]

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB()),
])
pipeline.fit(texts, labels)

request_counter = 0
new_texts = []
new_labels = []

@app.route('/predict', methods=['POST'])
def predict():
    global request_counter, new_texts, new_labels
    
    data = request.get_json()
    text = data['text']
    real_label = data.get('real_label', None)
    
    predicted_topic = pipeline.predict([text])[0]
    
    if real_label:
        new_texts.append(text)
        new_labels.append(real_label)
    
    request_counter += 1
    if request_counter % 80 == 0 and len(new_texts) > 0:
        threading.Thread(target=retrain_model).start()
        return jsonify({
            'prediction': predicted_topic,
            'message': 'Модель будет дообучена в фоновом режиме'
        })
    
    return jsonify({'prediction': predicted_topic})

def retrain_model():
    global pipeline, texts, labels, new_texts, new_labels
    
    print('Начинается переобучение модели')
    texts.extend(new_texts)
    labels.extend(new_labels)
    pipeline.fit(texts, labels)
    new_texts = []
    new_labels = []
    print('Модель успешно дообучена')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)