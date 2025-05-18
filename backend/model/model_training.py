import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
import numpy as np

def create_model(vocab_size, embedding_dim=64, lstm_units=128, dense_units=64, dropout_rate=0.5, num_classes=2, input_length=50): # Изменил num_classes=2
    model = Sequential([
        Embedding(vocab_size, embedding_dim, input_length=input_length),
        LSTM(lstm_units, return_sequences=True),
        LSTM(lstm_units // 2), # Уменьшил количество LSTM юнитов для второго слоя
        Dense(dense_units, activation='relu'),
        Dropout(dropout_rate),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model, X_train, y_train, X_test, y_test, epochs=10, batch_size=32):
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Точность на тестовых данных: {accuracy}")
    return model, history

def retrain_model(model, X_train, y_train, epochs=5, batch_size=32):
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)
    return model, history
if __name__ == "__main__":
    texts = ["пример текста 1", "пример текста 2"]
    labels = [0, 1]
    vocab_size = 1000  # Должно быть реальное значение
    model = create_model(vocab_size)
    X_train, X_test = np.random.rand(2, 50), np.random.rand(2, 50)  # Заглушки
    y_train, y_test = np.array([0, 1]), np.array([0, 1])
    model, history = train_model(model, X_train, y_train, X_test, y_test)

    model.save('trained_model.h5')
    print("Модель успешно сохранена")
