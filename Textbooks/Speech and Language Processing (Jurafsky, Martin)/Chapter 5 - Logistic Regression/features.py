"""Generates a feature matrix"""

from pathlib import Path
from math import log

pronouns = []

def positivecount(document):
    """Returns the count of positive lexicon words in the document"""
    count = 0
    with open(Path.cwd() / 'positivos.txt') as file:
        lexicon = file.read().splitlines()

    for word in document:
        for lexword in lexicon:
            if word.lower().strip() == lexword:
                count += 1
    
    return count

def negativecount(document):
    """Returns the count of negative lexicon words in the document"""
    count = 0
    with open(Path.cwd() / 'negativos.txt') as file:
        lexicon = file.read().splitlines()

    for word in document:
        for lexword in lexicon:
            if word.lower().strip() == lexword:
                count += 1
    
    return count

def contains_nao(document):
    """Returns 1 if the document contains the word 'não', or 0 otherwise"""
    for word in document:
        if word.lower().strip() == 'nao' or word.lower().strip() == 'não':
            return 1
    return 0

def pronouns_count(document):
    """Returns the count of 1st and 2nd person pronouns in the document"""
    pass

def contains_exclamation(document):
    """Returns 1 if the document contains an exclamation mark, 0 otherwise"""
    for word in document:
        if word == '!':
            return 1
    return 0

def logwordcount(document):
    """Returns the log of the word count of the document"""
    count = 0
    for word in document:
        if word.isalnum():
            count += 1
    return log(count)

def feature_vector(document):
    """Return a vector of features for the specified document"""
    return [positivecount(document), negativecount(document), 
            contains_nao(document), pronouns_count(document), 
            contains_exclamation(document), logwordcount(document)]

def feature_matrix(text):
    pass