import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def prepare_data(texts, labels, num_words=5000, maxlen=50, test_size=0.2, random_state=42):
    label_map = {label: i for i, label in enumerate(set(labels))}
    numerical_labels = [label_map[label] for label in labels]

    tokenizer = Tokenizer(num_words=num_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, padding='post', maxlen=maxlen)

    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, numerical_labels, test_size=test_size, random_state=random_state)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    import pickle
    with open('tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    with open('label_map.pkl', 'wb') as f:
        pickle.dump(label_map, f)
    print('файлы tokenzer.pkl and label_map.pkl сохранены')

    vocab_size = len(tokenizer.word_index) + 1

    return X_train, X_test, y_train, y_test, vocab_size, tokenizer, label_map
