import nltk
from nltk.stem.launcher import LancasterStemmer as lancst
import numpy as npbro
import tflearn as tfl
import tensorflow as tf
import json
import pickle as pick
import random

with open('intents.json') as intents:
    dat = json.load(intents)
stemmer = lancst()

words = []
labels = []
xdocs = []
ydocs = []

for intent in dat['intents']:
    for pat in intent['patterns']:
        words1 = nltk.word_tokenize(pat)
        words.extend(words1)
        xdocs.append(words1)
        ydocs.append(intent['tag'])
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in '?']
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []
outemp = [0 for _ in range(len(labels))]

for x, doc in enumerate(xdocs):
    bag = []
    words1 = [stemmer.stem(w) for w in doc]
    for w in words:
        if w in words1:
            bag.append(1)
        else:
            bag.append(0)

    outputrow = outemp[:]
    outputrow[labels.index(ydocs[x])] = 1
    training.append(bag)
    output.append(outputrow)

training = np.array(training)
output = np.array(output)
net = tfl.input_data(shape=[None, len(training[0])])
net = tfl.fully_connected(net, 10)
net = tfl.fully_connected(net, 10)
net = tfl.fully_connected(net, 10)
net = tfl.fully_connected(net, 10)
net = tfl.regression(net)

model = tfl.DNN(net)
model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)
model.save('model.tflearn')
def bagofwords(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for sw in s_words:
        for i, w in enumerate(words):
            if w == sw:
                bag[i] = 1
    return np.array(bag)

def chat(query):
    results = model.predict([bagofwords(query, words)])
    resultsind = np.argmax(results)
    tag = labels[resultsind]
    for tg in dat['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            return random.choice(responses)

def pchat(query):
    results = model.predict([bagofwords(query, words)])
    resultsind = np.argmax(results)
    tag = labels[resultsind]
    for tg in dat['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            return print(random.choice(responses))
