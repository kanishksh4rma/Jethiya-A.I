
will push the code and share the link. pehle bnana to shuru kru 😂😉
import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import colorama
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("intents.json") as file:
    data = json.load(file)


def chat():
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()
        if inp.lower() == "quit":
            break

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        #print(result)
        print('max : ',np.argmax(result))
        excuseme = ['kuch smjh me aaye aisa bol?','Mehta saheb, kitne kathin words ka use krte ho. yeh daya ko smjh me aaye aisa kuch bolo.','le phir se english']
        proper=True


        if np.argmax(result)<0:
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(excuseme))
            proper=False
        else:
            proper = True

        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        if proper:
            for i in data['intents']:
                if i['tag'] == tag:
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))

        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
chat()
