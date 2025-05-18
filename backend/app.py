from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os

app = Flask(__name__, static_folder='static')

# Загрузка модели и токенизатора
model = load_model('backend/model/trained_model.h5')
with open('backend/model/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
with open('backend/model/label_map.pkl', 'rb') as f:
    label_map = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data['text']
        
        # Преобразование текста в последовательность
        sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, padding='post', maxlen=50)
        
        # Предсказание
        prediction = model.predict(padded_sequence, verbose=0)
        predicted_index = np.argmax(prediction)
        
        # Обратное преобразование индекса в метку
        inverse_label_map = {i: label for label, i in label_map.items()}
        predicted_category = inverse_label_map[predicted_index]
        
        # Вероятности для всех категорий
        probabilities = {label: float(prediction[0][i]) for label, i in label_map.items()}
        
        return jsonify({
            'category': predicted_category,
            'probabilities': probabilities
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
