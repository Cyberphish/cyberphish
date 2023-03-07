import json
from flask import Flask, request, jsonify
import numpy as np
import pickle
import sklearn
import pandas as pd
import imblearn
import keras
from tensorflow.python.keras import models
from keras_preprocessing.sequence import pad_sequences

model = pickle.load(open('nb.pkl', 'rb'))
vec = pickle.load(open("vec.pkl", "rb"))
model = keras.models.load_model('spam_classifier_0.31.h5')
SEQUENCE_LENGTH = 100
tokenizer = pickle.load(open("tokenizer.pickle", "rb"))


app = Flask(__name__)

# declared an empty variable for reassignment
response = ''

def get_predictions(text):
    sequence = tokenizer.texts_to_sequences([text])
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=SEQUENCE_LENGTH)
    # get the prediction
    prediction = model.predict(sequence)[0]
    # one-hot encoded vector, revert using np.argmax
    return np.argmax(prediction)


@app.route('/', methods=['GET', 'POST'])
def pred():
    global response
    # checking the request type we get from the app
    if (request.method == 'POST'):
        print('inn')
        data = request.data
        request_data = json.loads(data.decode('utf-8'))
        subject = request_data['subject']
        body = request_data['body']
        features = "\n".join([subject, body])
        Vocab_list = {}
        encode = vec.transform([features]).toarray()
        #         bag_of_words = pd.DataFrame(
        #                encode, columns=vec.get_feature_names_out())


        #         for vector in bag_of_words:
        #            if (bag_of_words[vector].values > 0):
        #                Vocab_list[bag_of_words[vector].name] = bag_of_words[vector].values[0]
        #         prediction = model.predict(encode)
        prediction = get_predictions(vector)
        prediction = f'{prediction}'
        response = f'{Vocab_list}'        
        return jsonify({'prediction': prediction[1],
                        'vocabulary': response
                        }) 

    else:
        # sending data back to your frontend app
        subject = 'funds to share'
        body = "The University of Washington System is sharing funds for all students during this pandemic, please update your \n financial aid status to claim yours. \nLogin.uw.edu/covid-19-aid-update\n For instructions on Accepting Your Financial Aid on https://login.uw.edu/login/login./.\n Regards,\n Assistant Professor \nUniversity of Washington"
        Vocab_list = {}
        features = "\n".join([subject, body])
        Vocab_list = {}
        encode = vec.transform([features]).toarray()
        bag_of_words = pd.DataFrame(
               encode, columns=vec.get_feature_names_out())

        Vocab_list = {}

        for vector in bag_of_words:
           if (bag_of_words[vector].values > 0):
               Vocab_list[bag_of_words[vector].name] = bag_of_words[vector].values[0]
        prediction = model.predict(encode)
        prediction = f'{prediction}'
        response = f'{Vocab_list}'        
        return jsonify({'prediction': prediction[1],
                        'vocabulary': response
                        }) 
