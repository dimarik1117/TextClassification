from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import random
import threading
import training_date

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


def predict_and_retrain(text):
    global request_counter, pipeline, new_texts, new_labels, texts, labels
    predicted_topic = pipeline.predict([text])[0]

    real_label = input("Реальная категория (можете пропустить): ")

    if real_label:
        new_texts.append(text)
        new_labels.append(real_label)

    request_counter += 1
    if request_counter % 80 == 0 and len(new_texts) > 0:
        print("Дообучение модели...")

        threading.Thread(target=retrain_model).start()

        return "Дообучение..."

    return predicted_topic

def retrain_model():
    global pipeline, texts, labels, new_texts, new_labels
    print("Начинается переобучение...")
    texts.extend(new_texts)
    labels.extend(new_labels)
    pipeline.fit(texts, labels)
    new_texts = []
    new_labels = []
    print("Модель дообучена и готова к работе.")
while True:
    try:
        user_text = input("Ваш текст: ")
        if user_text.lower() == 'exit':
            break

        predicted_topic = predict_and_retrain(user_text)
        print(f"{predicted_topic}")

    except KeyboardInterrupt:
        print("\nЗавершение работы.")
        break