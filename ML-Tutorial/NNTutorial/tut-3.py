import tensorflow as tf
from tensorflow import keras
import numpy as np


def review_encode(s):
    encoded = [1]
    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded


data = keras.datasets.imdb
word_index = data.get_word_index()
word_index = {k:(v+3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3
model = keras.models.load_model("model.h5")
with open("movie-review.txt", encoding="utf-8") as f:
    for line in f.readlines():
        new_line = line
        for c in ",.()'':":
            new_line = new_line.replace(c, "")
        words_in_line = new_line.strip().split(" ")
        encode = review_encode(words_in_line)
        encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=250)
        predict = model.predict(encode)
        print(line)
        print(encode)
        print(predict[0])