# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

# Imports

import keras
from keras import Sequential
from keras.layers import LSTM, Dense, Dropout, Dropout, Activation, Flatten
from keras.losses import categorical_crossentropy
import numpy as np

# Sort

text = open("./localtrainingdata/motw.txt", "r").read()

chardict = sorted(list(set(text)))

total = len(text)
chars = len(chardict)

print("Total Charaters    :", total)
print("Total Unique Charaters :", chars)

# Format

chunklength = 75
step = 5
sentences = []
characters = []

for i in range(0, len(text) - chunklength, step):
	sentences.append(text[i : i + chunklength])
	characters.append(text[i + chunklength])

chunks = len(sentences)
print("Total Chunks       : ", chunks)

# Sample

print("Sample Chunk       : ", sentences[0])
print("Sample Character    : ", characters[0])

# Format

x = np.zeros(chunks * chunklength * chars, np.bool).reshape(chunks, chunklength, chars)
y = np.zeros(chunks * chars, np.bool).reshape(chunks, chars)

for i,v in enumerate(sentences):
	for a,b in enumerate(v):
		x[i][a][chardict.index(b)] = True

for i,v in enumerate(characters):
	y[i][chardict.index(v)] = True

print("Total Data Values  : ", chunks * chunklength * chars)
print("Total Label Values : ", chunks * chars)
print("X Shape :", x.shape)
print("Y Shape :", y.shape)

# Model

model = Sequential()
model.add(LSTM(4*  chars, return_sequences=True, input_shape=(chunklength, chars)))
model.add(Dense(2 * chars))
model.add(Dropout(0.2))
model.add(Dense(1 * chars))
model.add(Flatten())
model.add(Dense(chars))
model.add(Activation("softmax"))

model.summary()

model.compile(optimizer="rmsprop", loss=categorical_crossentropy)

# Load

#model = keras.models.load_model("././src/models/novelbot2")

# Train

model.fit(x=x, y=y, batch_size=chunklength, epochs=10)

# Save

model.save("./models/novelbot2")

# Prediction

inputdata = x[round(len(x)/2)].reshape(1, chunklength, chars)

prediction = model.predict(inputdata)

print("Input shape : ", inputdata.shape)

# Clean

totalprediction = ""
length = 50

print("Predicting the next : ", length, "characters.")

for i in range(length):
	prediction = model.predict(inputdata)
	textprediction = []
	arrayprediction = np.zeros(chars, np.bool).reshape(chars)

	for a in prediction:
		bi, bv = 1, -1
		for i,v in enumerate(a):
			if v > bv:
				bv = v
				bi = i
		textprediction.append(chardict[bi])
		arrayprediction[bi] = True

	inputdata[0] = np.append(inputdata[0][1:], arrayprediction).reshape(chunklength, chars)
	totalprediction += textprediction[0]

print(totalprediction)