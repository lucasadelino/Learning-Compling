from math import log
from pathlib import Path
from nbtokenizer import tokenize
import re

space_regex = re.compile(r"(\n)")

# This changes the number used for add-X smoothing.
A = 1

#TODO: It might be better if NB model is a class. Learn more about OO Python

"""
class_dict = {'negative': [['just', 'plain', 'boring'], 
                           ['entirely', 'predictable', 'and', 'lacks', 'energy'], 
                           ['no', 'surprises', 'and', 'very', 'few', 'laughs']],
              'positive': [['very', 'powerful'], 
                           ['the', 'most', 'fun', 'film', 'of', 'the', 'summer']]}

vocab = {'no': {'positive': 0.5, 'negative': 0.5},
        'khdd': {'positive': 0.2, 'negatve': 0.1}}

priors = {'positive': 0.3,
          'negative': 0.7}

class_word_counts = {'positive': {'word1': 8, 'word2': 4, 'word3': 2},
                     'negative': {'word1': 3, 'word2': 2, 'word3': 9}}
"""

def train(class_dict):
    """
    Trains the Naive Bayes classifier.
    """
    # Get n_doc value
    n_doc = 0
    for doc_list in class_dict.values():
        n_doc += len(doc_list)
    
    priors = {}
    classes_word_counts = {}
    for class_label, doc_list in class_dict.items():
        # Compute priors
        n_c = len(doc_list)    
        priors.update({class_label: log(n_c/n_doc)})

        # Generate dict with word counts for each class
        each_class_word_counts = {}
        for document in doc_list:
            for word in document:
                each_class_word_counts.setdefault(word, 0)
                each_class_word_counts[word] += 1

        classes_word_counts.update({class_label: each_class_word_counts})
    
    # Get vocab
    vocab = {}
    for dict in classes_word_counts.values():
        for key in dict.keys():
            vocab.setdefault(key, {})
    
    for class_label, word_count_dict in classes_word_counts.items():
        # Get total number of words of each class
        class_total_words = 0
        for value in word_count_dict.values():
            class_total_words += value
        
        # Compute likelihoods
        for word in vocab:
            word_count = word_count_dict.get(word, 0)
            formula = log((word_count + A) / (class_total_words + len(vocab)))
            vocab[word].update({class_label: formula})

    return (priors, vocab)

def test(test_doc, nb):
    """
    Tests a sentence against a NB classifier and returns the most likely class
    """
    sums = {}
    for class_label, prior in nb[0].items():
        this_sum = prior
        for word in test_doc:
            if word in nb[1]:
                this_sum += nb[1].get(word)[class_label]
        sums.update({class_label: this_sum})
    
    return max(sums, key=sums.get)

# TODO: Make this work with more than 1 class
def load_class_dict(cls1, cls2):
    """
    Returns a dictionary containing classes and documents that can be used in
    the naive Bayes classifier. Make sure to have .txt files with the same
    name passed to classes
    """
    with open(Path.cwd() / f'{cls1}.txt', 'r', encoding='utf-8') as file:
        cls1_docs = file.readlines()
        for i, item in enumerate(cls1_docs):
            if item == '\n':
                cls1_docs.pop(i)
        for i, item in enumerate(cls1_docs):
            cls1_docs[i] = space_regex.sub('', item)

    with open(Path.cwd() / f'{cls2}.txt', 'r', encoding='utf-8') as file:
        cls2_docs = file.readlines()
        for i, item in enumerate(cls2_docs):
            if item == '\n':
                cls2_docs.pop(i)
        for i, item in enumerate(cls2_docs):
            cls2_docs[i] = space_regex.sub('', item)

    cls1_docs = tokenize(cls1_docs, punctuation=False)
    cls2_docs = tokenize(cls2_docs, punctuation=False)

    return {cls1: cls1_docs, cls2: cls2_docs}

def bootstrap(test_set, num_samples):
    pass

class_dict = load_class_dict('positivo', 'negativo')

nb = train(class_dict)

string_to_test = 'tremores é um filme ruim'
tokenized_version = string_to_test.split(' ')
print(test(tokenized_version, nb))
