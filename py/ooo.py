import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import numpy as np

label_map = {label: i for i, label in enumerate(set(labels))}
numerical_labels = [label_map[label] for label in labels]

tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, padding='post', maxlen=50)
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, numerical_labels, test_size=0.2, random_state=42)
y_train = np.array(y_train)
y_test = np.array(y_test)

vocab_size = len(tokenizer.word_index) + 1

model = Sequential([
    Embedding(vocab_size, 64, input_length=50),
    LSTM(128, return_sequences=True),
    LSTM(64),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(set(labels)), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Точность на тестовых данных: {accuracy}")

def predict_category(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, padding='post', maxlen=50)
    prediction = model.predict(padded_sequence)
    predicted_index = np.argmax(prediction)
    # Инвертируем label_map для получения метки по индексу
    inverse_label_map = {i: label for label, i in label_map.items()}
    predicted_category = inverse_label_map[predicted_index]
    return predicted_category

new_text = ""
predicted_category = predict_category(new_text)
print(f"Предсказанная категория для текста '{new_text}': {predicted_category}")

model.save('text_categorization_model.h5')