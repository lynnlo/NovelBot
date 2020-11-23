# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

# Imports

import keras
from keras import Sequential
from keras.layers import LSTM, Dense, Dropout, Dropout, Activation, Reshape
from keras.losses import categorical_crossentropy
import numpy as np

# Sort

text = open("././src/data/other.txt", "r").read()

chardict = sorted(list(set(text)))

total = len(text)
chars = len(chardict)

print("Total Charaters    :", total)
print("Total Unique Charaters :", chars)

# Format

chunklength = 75
step = 1
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
y = np.zeros(chunks * 1 * chars, np.bool).reshape(chunks, 1, chars)

for i,v in enumerate(sentences):
	for a,b in enumerate(v):
		x[i][a][chardict.index(b)] = True

for i,v in enumerate(characters):
	y[i][0][chardict.index(v)] = True

print("Total Data Values  : ", chunks * chunklength * chars)
print("Total Label Values : ", chunks * 1 * chars)
print("X Shape :", x.shape)
print("Y Shape :", y.shape)

# Model

model = Sequential()
model.add(LSTM(2 * chars, return_sequences=True, input_shape=(chunklength, chars)))
model.add(Dense(chars))
model.add(Dropout(0.1))
model.add(Reshape((1, chunklength * chars)))
model.add(Dense(chars))
model.add(Activation("softmax"))

model.summary()

model.compile(optimizer="rmsprop", loss=categorical_crossentropy)

# Load

model = keras.models.load_model("././src/models/novelbot1")

# Train

#model.fit(x=x, y=y, batch_size=chunklength, epochs=5)

# Save

#model.save("././src/models/novelbot1")

# Prediction

inputdata = x[round(len(x)/2)].reshape(1, chunklength, chars)

prediction = model.predict(inputdata)[0]

print("Input shape : ", inputdata.shape)

# Clean

totalprediction = ""
length = 500

for i in range(length):

	cleaninput = []
	cleanprediction = []

	for a in prediction:
		bi, bv = 1, -1
		for i,v in enumerate(a):
			if v > bv:
				bv = v
				bi = i
		cleanprediction.append(chardict[bi])

	for a in inputdata:
		s = []
		for b in a:
			for i,v in enumerate(b):
				if v:
					s.append(chardict[i])
		cleaninput.append("".join(s))

	# New Prediction

	newinput = "".join(list(i for i in cleaninput[0])[1:]) + cleanprediction[0]

	userdata = np.zeros(chunklength * chars, np.bool).reshape(1, chunklength, chars)

	for i,v in enumerate(newinput):
		userdata[0][i][chardict.index(v)] = True
	inputdata = userdata

	prediction = model.predict(inputdata)[0]

	totalprediction += cleanprediction[0]

print(totalprediction)