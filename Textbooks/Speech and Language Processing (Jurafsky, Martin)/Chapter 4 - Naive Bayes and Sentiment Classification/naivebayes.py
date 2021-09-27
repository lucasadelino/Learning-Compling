from math import log

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
    for value in class_dict.values():
        n_doc += len(value)
    
    priors = {}
    class_word_counts = {}
    for key, value in class_dict.items():
        # Compute priors
        n_c = len(value)    
        priors.update({key: log(n_c/n_doc)})

        # Get word counts by class
        class_vocab = {}
        for document in value:
            for word in document:
                class_vocab.setdefault(word, 0)
                class_vocab[word] += 1
        class_word_counts.update({key: class_vocab})
    
    # Get vocab
    vocab = {}
    for dict in class_word_counts.values():
        for key in dict.keys():
            vocab.setdefault(key, {})
    
    for keye, dict in class_word_counts.items():
        # Get total word counts by class
        class_total_words = 0
        for value in dict.values():
            class_total_words += value
        
        # Compute likelihoods
        for key in vocab:
            countiee = dict.get(key, 0)
            formula = log((countiee + 1) / (class_total_words + len(vocab)))
            vocab[key].update({keye: formula})

    return (priors, vocab)

def test(test_doc, training_tuple):
    """
    Tests a sentence agains a NB classifier and returns the most likely class
    """
    sums = {}
    for label, prior in training_tuple[0].items():
        this_sum = prior
        for word in test_doc:
            if word in training_tuple[1]:
                this_sum += training_tuple[1].get(word)[label]
        sums.update({label: this_sum})
    
    return max(sums, key=sums.get)

def bootstrap(test_set, samples):
    return

class_dict = {'negative': [['just', 'plain', 'boring'], 
                           ['entirely', 'predictable', 'and', 'lacks', 'energy'], 
                           ['no', 'surprises', 'and', 'very', 'few', 'laughs']],
              'positive': [['very', 'powerful'], 
                           ['the', 'most', 'fun', 'film', 'of', 'the', 'summer']]}

nb = train(class_dict)
print(test(['very', 'fun'], nb))