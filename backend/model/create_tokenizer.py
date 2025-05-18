import pickle
from tensorflow.keras.preprocessing.text import Tokenizer

# 1. Инициализация токенизатора
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")

# 2. Пример текстов для обучения (замените на ваши реальные данные)
texts = [
    "Пример текста о футболе",
    "Другой текст про технологии",
    "Третий пример про погоду"
]

# 3. Обучение токенизатора
tokenizer.fit_on_texts(texts)

# 4. Создание label_map (замените на ваши реальные категории)
label_map = {"футбол": 0, "технологии": 1, "погода": 2}

# 5. Сохранение файлов
with open('backend/model/tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
    
with open('backend/model/label_map.pkl', 'wb') as f:
    pickle.dump(label_map, f)

print("Файлы tokenizer.pkl и label_map.pkl успешно созданы!")
