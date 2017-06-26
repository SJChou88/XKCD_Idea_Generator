from __future__ import print_function

import flask
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
import random
import pickle
#---------- MODEL IN MEMORY ----------------#

ix_to_char = pickle.load( open( "vocab.p", "rb" ) )
VOCAB_SIZE = len(ix_to_char)
WEIGHTS = 'checkpoint_layer_3_hidden_700_epoch_350.hdf5'
VOCAB_SIZE = 112
ix_to_char = {0: '\n',
 1: ' ',
 2: '!',
 3: '"',
 4: '#',
 5: '$',
 6: '%',
 7: '&',
 8: "'",
 9: '(',
 10: ')',
 11: '*',
 12: '+',
 13: ',',
 14: '-',
 15: '.',
 16: '/',
 17: '0',
 18: '1',
 19: '2',
 20: '3',
 21: '4',
 22: '5',
 23: '6',
 24: '7',
 25: '8',
 26: '9',
 27: ':',
 28: ';',
 29: '<',
 30: '=',
 31: '>',
 32: '?',
 33: 'A',
 34: 'B',
 35: 'C',
 36: 'D',
 37: 'E',
 38: 'F',
 39: 'G',
 40: 'H',
 41: 'I',
 42: 'J',
 43: 'K',
 44: 'L',
 45: 'M',
 46: 'N',
 47: 'O',
 48: 'P',
 49: 'Q',
 50: 'R',
 51: 'S',
 52: 'T',
 53: 'U',
 54: 'V',
 55: 'W',
 56: 'X',
 57: 'Y',
 58: 'Z',
 59: '[',
 60: '\\',
 61: ']',
 62: '^',
 63: '_',
 64: 'a',
 65: 'b',
 66: 'c',
 67: 'd',
 68: 'e',
 69: 'f',
 70: 'g',
 71: 'h',
 72: 'i',
 73: 'j',
 74: 'k',
 75: 'l',
 76: 'm',
 77: 'n',
 78: 'o',
 79: 'p',
 80: 'q',
 81: 'r',
 82: 's',
 83: 't',
 84: 'u',
 85: 'v',
 86: 'w',
 87: 'x',
 88: 'y',
 89: 'z',
 90: '{',
 91: '|',
 92: '}',
 93: '~',
 94: '\xa0',
 95: '®',
 96: '°',
 97: 'ä',
 98: 'é',
 99: 'ö',
 100: 'π',
 101: '–',
 102: '—',
 103: '’',
 104: '“',
 105: '”',
 106: '•',
 107: '…',
 108: '→',
 109: '★',
 110: '☐',
 111: '雨'}


BATCH_SIZE = 50
HIDDEN_DIM = 700
SEQ_LENGTH = 90

GENERATE_LENGTH = 500
LAYER_NUM = 3

model = Sequential()
model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))

for i in range(LAYER_NUM - 1):
    model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(VOCAB_SIZE)))
model.add(Activation('softmax'))
model.compile(loss="categorical_crossentropy", optimizer="rmsprop")
model.load_weights(WEIGHTS)

#------------- Functions -----------------#


def weighted_choice(choices):
    choices2 = [x if x >= .1 else 0 for x in choices]
    total = sum(w for c, w in enumerate(choices2))
    r = random.uniform(0, total)
    upto = 0
    for c, w in enumerate(choices2):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
    
def generate_text_prompt(model, length, vocab_size, ix_to_char, prompt):
    X = np.zeros((1, len(prompt) + length, vocab_size))
    y_char=[]
    for i,p in enumerate(prompt):
        for ix1, char in ix_to_char.items():
            if char == p:
                ix =[ix1]
        X[0, i, :][ix[-1]] = 1
        print(ix_to_char[ix[-1]], end="")
        y_char.append(ix_to_char[ix[-1]])

    for i2 in range(length):
        a = model.predict(X[:, :i2 + len(prompt), :])[0][-1]
        ix = weighted_choice(a)
        X[0, i2 + len(prompt), :][ix] = 1
        print(ix_to_char[ix], end="")
        y_char.append(ix_to_char[ix])               
    return ('').join(y_char)



#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("awesome.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/generate", methods=["POST"])
def generate():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    data = flask.request.get_json(force=True)
    seed=data["seed"]
    GENERATE_LENGTH=int(data["length"])
    generated_text = generate_text_prompt(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char, seed)
    results = {"text": generated_text}
    return flask.jsonify(results)


#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0', debug=True)
