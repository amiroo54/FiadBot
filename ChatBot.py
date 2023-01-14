import nltk
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import hazm
import os
words = []
tags = []
docs_x = []
docs_y = []
data = ''
#def StartTheModel():
with open("intents.json") as file:
        data = json.load(file)
        
try:
    with open("data.pickle", "rb") as f:
        words, tags, training, output = pickle.load(f)
except:
    words = []
    tags = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = hazm.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in tags:
            tags.append(intent["tag"])

    words = sorted(list(set(words)))

    tags = sorted(tags)

    output = []
    training = []

    out_empty = [0 for _ in range(len(tags))]

    for x,doc in enumerate(docs_x):
        bag = []
        for w in words:
            if w in doc:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[tags.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)
        
        
        
    training = numpy.array(training)
    output = numpy.array(output)
    
    with open("data.pickle", "wb") as f:
        pickle.dump((words, tags, training, output), f)

net = tflearn.input_data(shape=[None,len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation = "softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

if os.path.exists("model.tflearn.meta"):
    model.load("model.tflearn") 
else:
    model.fit(training, output, n_epoch=1000, batch_size = 8, show_metric = True)
    model.save("model.tflearn")
#return model
        
    
def BagOfWords(s):
    bag = [0 for _ in range(len(words))]
    s_words = hazm.word_tokenize(s)
    for word in s_words:
        for i, w in enumerate(words):
            if w == word:
                bag[i] = 1 
            print(bag[i])

    return numpy.array(bag)
    


def GiveRsponse(s):#, model):
    result = model.predict([BagOfWords(s)])
    result_index = numpy.argmax(result)
    tag = tags[result_index]
    for tg in data["intents"]:
        if tg['tag'] == tag:
            resposes = tg['responses']   
    
    return random.choice(resposes) 

print(GiveRsponse("سلام"))