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
    model = keras.models.load_model('chat_model.h5')
    max_len = 25

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()
        inp = inp.lower()
        if inp.lower() == "quit":
          print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , "Aapko humse rishta nahi rakhna koi baat nahi, meri taraf se bhi koi jabarjasti nahi hai")
          break

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        print(sorted(result))

        #print('max : ',np.argmax(result))
        excuseme = ['kuch smjh me aaye aisa bol?','Mehta saheb, kitne kathin words ka use krte ho. yeh daya ko smjh me aaye aisa kuch bolo.','le phir se english']
        proper=True


        if np.argmax(result)<0:
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(excuseme))
            proper=False
        else:
            proper = True

        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        from test import retTestCase,updateTestCases
        if proper:
            for i in data['intents']:
                if i['tag'] == tag:
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))
                    #print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL ,'Satisfy ? : ',end="")
                    #Satisfy = int(input())
                    Satisfy=False
                    if Satisfy:

                        input_lst,output = retTestCase()

                        if inp not in input_lst:
                            newInput = inp
                            newOutput = np.argmax(result)
                            updateTestCases('test_cases.csv',[newInput,newOutput])

        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)
chat()
