# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

from keras import Sequential
from keras import models
from keras.layers import LSTM, Dense, Dropout, Flatten, Activation, Reshape
from keras.losses import categorical_crossentropy
from sklearn import preprocessing
import numpy as np

text = open("data/other.txt", "r").read()

chardict = sorted(list(set(text)))

total = len(text)
chars = len(chardict)

print("Total Charaters        :", total)
print("Total Unique Charaters :", chars)

chunklength = 100
step = 5
sentences = []
characters = []

for i in range(0, len(text) - chunklength, step):
    sentences.append(text[i : i + chunklength])
    characters.append(text[i + chunklength])

chunks = len(sentences)
print("Total Chunks :", chunks)

x = np.zeros(chunks * chunklength * chars, np.bool).reshape(chunks, chunklength, chars)
y = np.zeros(chunks * 1 * chars, np.bool).reshape(chunks, chars)

for i,v in enumerate(sentences):
    for a,b in enumerate(v):
        x[i][a][chardict.index(b)] = True

for i,v in enumerate(characters):
    y[i][chardict.index(v)] = True

print("Total Data Values  : ", chunks * chunklength * chars)
print("Total Label Values : ", chunks * chars)
print("X Shape :", x.shape)
print("Y Shape :", y.shape)

model = Sequential()
model.add(LSTM(2 * chars, return_sequences=True, input_shape=(chunklength, chars)))
model.add(Dense(chars))
model.add(Flatten())
model.add(Dense(chars, dtype="float64"))
model.add(Activation("softmax", dtype="float64"))

model.summary()

model.compile(optimizer="rmsprop", loss=categorical_crossentropy)

model = models.load_model("models/novelbot2-4")

model.fit(x=x, y=y, batch_size=chunklength, epochs=60)

userinput = "Hello there, I am"

userdata = np.zeros(chunklength * chars, np.bool).reshape(1, chunklength, chars)

for i,v in enumerate(userinput):
        userdata[0][i][chardict.index(v)] = True

inputdata = x[2000].reshape(1, chunklength, chars)

print("Input shape : ", inputdata.shape)

totalclean = ""

for i in range(chunklength * 5):
    prediction = model.predict(inputdata).astype("float64")
    prediction = np.random.multinomial(1, prediction[0], 1)

    for a,b in enumerate(prediction[0]):
        if b == 1:
            prediction[0][a] = True
            totalclean += chardict[a]
        else:
            prediction[0][a] = False

    inputdata[0] = np.append(inputdata[0][1:], prediction).reshape(chunklength, chars)


print(totalclean)
print("\n\n")

model.save("models/novelbot2-4")
