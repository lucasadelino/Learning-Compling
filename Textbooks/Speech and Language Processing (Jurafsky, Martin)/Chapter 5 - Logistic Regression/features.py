"""Generates a feature matrix"""

def positivecount(document):
    """Returns the count of positive lexicon words in the document"""
    pass

def negativecount(document):
    """Returns the count of negative lexicon words in the document"""
    pass

def contains_nao(document):
    """Returns 1 if the document contains the word 'não', or 0 otherwise"""
    pass

def pronouns_count(document):
    """Returns the count of 1st and 2nd person pronouns in the document"""
    pass

def logwordcount(document):
    """Returns the log of the word count of the document"""
    pass

def feature_vector(document):
    return [positivecount(document), negativecount(document), 
            contains_nao(document), pronouns_count(document), 
            logwordcount(document)]

def feature_matrix(text):
    pass