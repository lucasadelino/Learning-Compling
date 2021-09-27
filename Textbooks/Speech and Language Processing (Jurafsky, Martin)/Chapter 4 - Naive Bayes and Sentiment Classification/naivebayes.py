"""
Implementing this was a fun challenge! This code works, but is very messy. 
Nevertheless, I wanted to preserve this first version to serve as reference for
how I will (hopefully) improve and clean up the code.

Here's what I did to help myself figure out how to implement this:

I knew the code would require a lot of iteration, so I made several 'for' 
loops -- even if they were redundant. My priority was to understand what needed 
to happen in each iteration, so that later, when I had that figured out, I 
could collapse any redundant loops together.

I made example dictionaries (in comments throughout the code) just so I was 
100% sure how each dictionary would be structured. These really helped! 
Whenever I was unsure of what to do in an iterator, I looked to them for 
reference.

I used random variable names just to keep the flow of writing going. I realize
these can be confusing, but stopping to think of a better name would interrupt
my train of thought.

All of these things introduced considerable bloat to the code, but they helped
me get the job done. My focus is now on cleaning up and commentating. 
"""

from math import log, exp

# class_list = [{'label': 'positive', 'documents': ['doc1', 'doc2'...]},
#               {'label': 'negative', 'documents': ['doc1', 'doc2'...]}]

"""
vocab = {'no': {'positive': 0.5, 'negative': 0.5},
        'khdd': {'positive': 0.2, 'negatve': 0.1}}

priors = {'positive': 0.3,
          'negative': 0.7}

"""

def wordcount(word_dict, token_list):
    for word in token_list:
        word_dict.setdefault(word, 0)
        word_dict[word] += 1
    return word_dict

def train(class_list):
    
    n_doc = 0
    for each_class in class_list:
        n_doc += len(each_class['documents'])
    
    priors = {}
    for each_class in class_list:
        n_c = len(each_class['documents'])    
        priors.update({each_class['label']: log(n_c/n_doc)})
        
    # class_list = [{'label': 'positive', 'documents': ['doc1', 'doc2'...]},
    #               {'label': 'negative', 'documents': ['doc1', 'doc2'...]}]
    
    class_word_counts = {}
    for each_class in class_list:
        class_vocab = {}
        for document in each_class['documents']:
            wordcount(class_vocab, document)
        class_word_counts.update({each_class['label']: class_vocab})

    """
    class_word_counts = {'positive': {'word1': 8, 'word2': 4, 'word3': 2},
                         'negative': {'word1': 3, 'word2': 2, 'word3': 9}}
    """
    """
    vocab = {'no': {'positive': 0.5, 'negative': 0.5},
             'khdd': {'positive': 0.2, 'negatve': 0.1}}
        """
    
    vocab = {}
    for dict in class_word_counts.values():
        for key in dict.keys():
            vocab.setdefault(key, {})
    
    vocabsize = len(vocab)
    
    for keye, dictie in class_word_counts.items():
        class_total_words = 0
        for value in dictie.values():
            class_total_words += value
        
        for key in vocab:
            countiee = dictie.get(key, 0)
            formula = log((countiee + 1) / (class_total_words + vocabsize))
            vocab[key].update({keye: formula})

    return (priors, vocab)

def test(testdoc, logprior, loglikelihood, c, v):
    return

def bootstrap(test_set, samples):
    return 

class_list = [{'label': 'negative', 'documents': [['just', 'plain', 'boring'], 
                                                  ['entirely', 'predictable', 'and', 'lacks', 'energy'], 
                                                  ['no', 'surprises', 'and', 'very', 'few', 'laughs']]},
              {'label': 'positive', 'documents': [['very', 'powerful'], 
                                                  ['the', 'most', 'fun', 'film', 'of', 'the', 'summer']]}]

print(train(class_list))