#from features import feature_matrix
from pathlib import Path
from tkinter import Y
from nbtokenizer import tokenize
from features import feature_matrix
from random import randint
import numpy as np
import re

MIN_STEPSIZE = 0.0001

LEARNING_RATE = 0.05

space_regex = re.compile(r"(\n)")

def load_class_list(cls1, cls0):
    """
    Helper function that creates a list of classes from  two text files. Uses 
    the name of the text files as the name of each class 
    """
    with open(Path.cwd() / f'{cls1}.txt', 'r', encoding='utf-8') as file:
        cls1_docs = file.readlines()
        for i, item in enumerate(cls1_docs):
            if item == '\n':
                cls1_docs.pop(i)
        for i, item in enumerate(cls1_docs):
            cls1_docs[i] = space_regex.sub('', item)

    with open(Path.cwd() / f'{cls0}.txt', 'r', encoding='utf-8') as file:
        cls0_docs = file.readlines()
        for i, item in enumerate(cls0_docs):
            if item == '\n':
                cls0_docs.pop(i)
        for i, item in enumerate(cls0_docs):
            cls0_docs[i] = space_regex.sub('', item)

    cls1_docs = tokenize(cls1_docs, punctuation=True)
    cls0_docs = tokenize(cls0_docs, punctuation=True)

    docs = cls1_docs + cls0_docs
    y = [1] * len(cls1_docs) + [0] * len(cls0_docs)

    return (docs, y)

def get_sublist(batch_size, class_list):
    """Helper function that creates a list out of x elements of a bigger list. 
    Useful for mini-batch gradient descent"""
    original_docs, original_y = class_list

    # Get a batch and generate batch y
    batch = []
    y = []
    
    # This will keep track of indexes we already chose, to avoid choosing the 
    # same document twice
    chosen_indexes = []
    for _ in range(batch_size):
        index = randint(0, len(original_docs) - 1)
        if index not in chosen_indexes:
            chosen_indexes.append(index)
            batch.append(original_docs[index])
            y.append(original_y[index])
    
    return(batch, [y])
            
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

"""def gradient(X, w, b, y):
    w_gradients = (np.dot((sigmoid(np.dot(X, w) + b) - y).T, X)) / len(y)
    b_gradients = (sigmoid(np.dot(X, w) + b) - y) / len(y)

    return (w_gradients, b_gradients)
"""

def minibatch_gdescent(X, w, b, y):
    """Perform gradient descent for a mini batch features X"""    
    # Calculate average gradients
    steps = 0
    while True:
        steps += 1

        # Get gradients
        w_gradients = np.dot((sigmoid(np.dot(X, w) + b) - y).T, X) / len(y)
        b_gradients = (sigmoid(np.dot(X, w) + b) - y) / len(y)

        # Use gradients to calculate new parameters
        w_step = LEARNING_RATE * w_gradients.T
        b_step = LEARNING_RATE * b_gradients
        w = w - w_step
        b = b - b_step

        if steps > 10000 or np.all(np.abs(w_step) < MIN_STEPSIZE):
            break
    
    print('Took ' + str(steps) + ' steps.')
    print(w_step)
    return (w, b)

# Initialize w and b as zeros
w = [[0, 0, 0, 0, 0, 0]]

b = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

sublist, y = get_sublist(32, load_class_list('positivo', 'negativo'))
X = np.array(feature_matrix(sublist))
y = np.array(y).T
w = np.array(w).T
b = np.array(b).T
w, b = minibatch_gdescent(X, w, b, y)
print(w)