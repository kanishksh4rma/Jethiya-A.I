import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import argparse



class JethiyaAI():
    """class for JethiyaAI."""

    def __init__(self,epochs,vocab_size,max_len):
        print("❥"*33)
        print(">Initializing ChatBot ...")
        self.max_len = max_len
        self.epochs = epochs
        self.vocab_size = vocab_size
        print(
        """


░░░░░██╗███████╗████████╗██╗░░██╗██╗██╗░░░██╗░█████╗░░░░░░░░█████╗░░░░██╗
░░░░░██║██╔════╝╚══██╔══╝██║░░██║██║╚██╗░██╔╝██╔══██╗░░░░░░██╔══██╗░░░██║
░░░░░██║█████╗░░░░░██║░░░███████║██║░╚████╔╝░███████║█████╗███████║░░░██║
██╗░░██║██╔══╝░░░░░██║░░░██╔══██║██║░░╚██╔╝░░██╔══██║╚════╝██╔══██║░░░██║
╚█████╔╝███████╗░░░██║░░░██║░░██║██║░░░██║░░░██║░░██║░░░░░░██║░░██║██╗██║
░╚════╝░╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░░░░░╚═╝░░╚═╝╚═╝╚═╝



        """
        )
        print("❥"*33)

    def buildModel(self):
      with open('intents.json',encoding='utf-8', errors='ignore') as file:
            data = json.load(file, strict=False)

      training_sentences = []
      training_labels = []
      labels = []
      responses = []

      for intent in data['intents']:
          for pattern in intent['patterns']:
              training_sentences.append(str(pattern).lower())
              training_labels.append(str(intent['tag']))
          responses.append(str(intent['responses']).lower())

          if intent['tag'] not in labels:
              labels.append(str(intent['tag']))

      num_classes = len(labels)

      lbl_encoder = LabelEncoder()
      lbl_encoder.fit(training_labels)
      training_labels = lbl_encoder.transform(training_labels)

      
      embedding_dim = 16
      
      oov_token = "<OOV>"

      tokenizer = Tokenizer(num_words=self.vocab_size, oov_token=oov_token)
      tokenizer.fit_on_texts(training_sentences)
      word_index = tokenizer.word_index
      sequences = tokenizer.texts_to_sequences(training_sentences)
      padded_sequences = pad_sequences(sequences, truncating='post', maxlen=self.max_len)

      model = Sequential()
      model.add(Embedding(self.vocab_size, embedding_dim, input_length=self.max_len))
      model.add(GlobalAveragePooling1D())
      model.add(Dense(16, activation='relu'))
      model.add(Dense(16, activation='relu'))
      model.add(Dense(num_classes, activation='softmax'))

      model.compile(loss='sparse_categorical_crossentropy',
                    optimizer='adam', metrics=['accuracy'])

      model.summary()
      
      checkpoint_filepath = 'chat_model_checkpoint.h5'
      model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
          filepath=checkpoint_filepath,
          save_weights_only=True,
          monitor='val_loss',
          mode='max',
          save_best_only=True)

      # Model weights are saved at the end of every epoch, if it's the best seen
      # so far.
      model.fit(padded_sequences, np.array(training_labels), epochs=self.epochs, callbacks=[model_checkpoint_callback])
      model.save(checkpoint_filepath)
      model.save("chat_model.h5")

      # to save the fitted tokenizer
      with open('tokenizer.pickle', 'wb') as handle:
          pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

      # to save the fitted label encoder
      with open('label_encoder.pickle', 'wb') as ecn_file:
          pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

      return model

    # test function to perform a automated test!
    def test(self,input_lst,output):

      self.buildModel()
      # load trained model
      model = keras.models.load_model('chat_model.h5')
      # load tokenizer object
      with open('tokenizer.pickle', 'rb') as handle:
          tokenizer = pickle.load(handle)

      # load label encoder object
      with open('label_encoder.pickle', 'rb') as enc:
          lbl_encoder = pickle.load(enc)

      # parameters
      
      res = []
      for inp in input_lst:
          result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                              truncating='post', maxlen=self.max_len))
          #print(result)
          #print('max : ',np.argmax(result))
          res.append(np.argmax(result))
      count = 0
      wrongTag = []
      for i in res:
          for j in output:
              if str(i) == str(j):
                  count += 1
                  break
              else:
                  wrongTag.append(str(lbl_encoder.inverse_transform([np.argmax(result)])))
      return (count,wrongTag)

#model.load_weights(checkpoint_filepath)
#history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)
if __name__ == '__main__':

  my_parser = argparse.ArgumentParser(description='Epochs and vocab_size')

  # Add the arguments
  my_parser.add_argument('-e','--epochs',
                        metavar='epochs',
                        type=int,
                        help='the epochs',default=2400)
  my_parser.add_argument('-v','--vocab_size',
                        metavar='vocab_size',
                        type=int,
                        help='the vocab_size',default=1000)

  # Execute the parse_args() method
  args = my_parser.parse_args()
 
  #babuchakEngine = JethiyaAI(epochs=2400,vocab_size=1000,max_len=25)
  babuchakEngine = JethiyaAI(epochs=args.epochs,vocab_size=args.vocab_size,max_len=25)
  babuchakEngine.buildModel()
