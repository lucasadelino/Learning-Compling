from math import log
from pathlib import Path
from nbtokenizer import tokenize
import re

space_regex = re.compile(r"(\n)")

# This changes the number used for add-X smoothing.
A = 1

class NaiveBayes:
    def __init__(self):

        self.class_dict = {}
        
        # class_dict = {
        #   'negative': [['just', 'plain', 'boring'], 
        #                ['entirely', 'predictable', 'and', 'lacks', 'energy'], 
        #                ['no', 'surprises', 'and', 'very', 'few', 'laughs']],
        #   'positive': [['very', 'powerful'], 
        #                ['the', 'most', 'fun', 'film', 'of', 'the', 'summer']]
        #             }
        

        self.likelihoods = {}
        # likelihoods = {'no': {'positive': 0.5, 'negative': 0.5},
        #                'just': {'positive': 0.2, 'negatve': 0.1}}

        self.priors = {}
        # priors = {'positive': 0.3,
        #           'negative': 0.7}

        self.totalwords = 0

    def load_class_dict(self, cls1, cls2):
        """
        Helper function that creates a dictionary of classes from  two text 
        files. Uses the name of the text files as the name of each class 
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

        self.class_dict = {cls1: cls1_docs, cls2: cls2_docs}


    def train(self, cls1, cls2):
        """
        Trains the Naive Bayes classifier.
        """

        self.load_class_dict(cls1, cls2)

        # Get number of documents (for both classes)
        n_doc = 0
        for doc_list in self.class_dict.values():
            n_doc += len(doc_list)
        
        classes_word_counts = {}
        # class_word_counts = {'positive': {'she': 8, 'set': 4, 'out': 2},
        #                      'negative': {'she': 3, 'did': 2, 'say': 9}}

        for class_label, doc_list in self.class_dict.items():
            # Compute priors
            n_c = len(doc_list)    
            self.priors.update({class_label: log(n_c/n_doc)})

            # Generate dict with word counts for each class
            each_class_word_counts = {}
            for document in doc_list:
                for word in document:
                    each_class_word_counts.setdefault(word, 0)
                    each_class_word_counts[word] += 1
                    self.totalwords += 1

            classes_word_counts.update({class_label: each_class_word_counts})
        
        # Get vocab
        for dict in classes_word_counts.values():
            for key in dict.keys():
                self.likelihoods.setdefault(key, {})
        
        for class_label, word_count_dict in classes_word_counts.items():
            # Get total number of words of each class
            class_total_words = 0
            for value in word_count_dict.values():
                class_total_words += value
            
            # Compute likelihoods
            for word in self.likelihoods:
                word_count = word_count_dict.get(word, 0)
                formula = log((word_count + A) / (class_total_words + len(self.likelihoods)))
                self.likelihoods[word].update({class_label: formula})

    def test(self, test_doc):
        """
        Tests a sentence against a NB classifier and returns the most likely class
        """
        sums = {}
        for class_label, prior in self.priors.items():
            this_sum = prior
            for word in test_doc:
                if word in self.likelihoods:
                    this_sum += self.likelihoods.get(word)[class_label]
            sums.update({class_label: this_sum})
        
        return max(sums, key=sums.get)

    def bootstrap(test_set, num_samples):
        pass
