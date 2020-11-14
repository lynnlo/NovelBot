from keras.layers import Dense, Activation, LSTM
import numpy as np
import matplotlib as mp

text = open("data/romeoandjuliet.txt", "r").read()

chars = sorted(text)

chucklength = 60
step = 5
sentences = []
characters = []

for i in range(0, len(text) - chucklength, step):
    sentences.append(text[i:i+chucklength])
    characters.append(text[i + chucklength])



