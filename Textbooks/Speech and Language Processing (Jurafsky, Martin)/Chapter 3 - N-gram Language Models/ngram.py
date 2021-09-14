"""
Contains functions to build ngram language models
TODO: Create ngram probability function
"""

import re
import math
from random import choices

# Matches everything before a period, question mark, or exclamation mark. 
sentence_regex = re.compile(r'(\S(?:.+?)[\.\?!]+)')

# Matches either a sequence of word characters or a punctuation mark
token_regex = re.compile(r'(\w+|[“”":;\'-\.\?!,]+)')

# Matches punctuation marks
punctuation_regex = re.compile(r'([“”":;\'-\.\?!,]+)') 

# Matches en dashes surrounded by word characters. Useful for PT-BR parsing
travessao_regex = re.compile(r'(\w)-(\w)')

# TODO: Read example text from a .txt file
example_text = 'César, Augusto, Nero e Massinissa, com os nomes por baixo... Não alcanço a razão de tais personagens.'

def sentence_segment(text):
    """Returns a list containing the argument text broken up into sentences. 
    Uses sentence_regex to look for sentences.
    """
    return list(sentence_regex.findall(text))

# TODO: Separate tokenizer into another file
def tokenize(text, punctuation = True, n = 1):
    """
    A very crude tokenizer. Returns a list of tokens for each sentence in the 
    text passed as argument. Punctuation marks are considered tokens if the 
    'punctuation' argument is set to True, or deleted if punctuation is set to 
    False. The n parameter adds n - 1 sentence start <s> and end </s> markers
    to each sentence for ngram processing. At present, this tokenizer doesn't 
    take named entities into account or employs any normalization other than 
    case folding.
    TODO: Add option that returns a single list instead of a list of lists
    """
    sentence_list = sentence_segment(text)

    # This will contain a list for each sentence to be tokenized
    token_list = []
    
    if punctuation == True:
        for sentence in sentence_list:
            token_list.append(token_regex.findall(sentence))
    else:
        for i, sentence in enumerate(sentence_list):
            # First, sub any en dashes for spaces (for PT-BR parsing)
            sentence_list[i] = travessao_regex.sub(r'\1 \2', sentence)
            # Then, remove any remaining punctuation
            sentence_list[i] = punctuation_regex.sub('', sentence_list[i])
            
            token_list.append(sentence_list[i].split(' '))
    
    # Case fold all words to lowercase
    for each_list in token_list:
        for i, word in enumerate(each_list):
            if word.isupper() or word.istitle():
                each_list[i] = word.lower()

    # Insert sentence start <s> and end </s> markers into each list of tokens
    if n > 1:
        for i, sentence in enumerate(token_list):
            token_list[i] = (['<s>']*(n - 1)) + sentence + (['</s>']*(n - 1))

    return token_list

def ngram_count(n, token_list):
    """
    Counts the ngrams in a list of tokens. Returns a dictionary in which 
    key-value pairs are, respectively, each ngram and how many times it appears
    in the list.
    """
    # Since an ngram looks n - 1 words into the past, we'll call this value 'm'
    m = n - 1

    ngram_dict = {}

    for sentence in token_list:
        for i in range(m, len(sentence)):
            # Look at last (i - m) words for concatenation
            pointer = i - m
            # Form an ngram by concatenating last (i - m) words, up to i
            ngram = ''
            while pointer <= i: 
                ngram += sentence[pointer] + ' '
                pointer += 1
            # Strip trailing whitespace and add ngram to dict
            ngram = ngram.rstrip()
            ngram_dict.setdefault(ngram, 0)
            ngram_dict[ngram] += 1
    
    return ngram_dict

def ngram_prob(n, token_list):
    """
    Generates Maximum Likelihood Estimation probabilities of the ngrams present
    in a list of tokens. Returns a dictionary in which key-value pairs are,
    respectively, each ngram and its probability
    """    
    # This will contain the ngrams and their probabilities
    ngram_prob = {}
    
    # Generate list containing lower order (n-1)gram and ngram.
    ngram_counts_list = [
        ngram_count(n - 1, token_list),
        ngram_count(n, token_list)
    ]

    for key, count in ngram_counts_list[1].items():
        # Lower order ngram = current ngram minus its last word
        lower_ngram_key = key.rsplit(' ', 1)[0]
        lower_ngram_count = ngram_counts_list[0][lower_ngram_key]
        p = count / lower_ngram_count
        ngram_prob.update({key: p})
    
    return ngram_prob

def generate_sentence(ngram_prob):
    """
    Generates a sentence based on a dictionary of ngram probabilities
    """
    # Look at keys in ngram_prob to figure out what's the order of our ngrams
    n = len(list(ngram_prob.keys())[0].split(' '))
       
    # Look for 1st ngram. Consider only ngrams that start with n-1 <s> markers
    next_keys = []
    next_values = []
    start_marker = ('<s> ' * (n - 1)).strip()
    for k, v in ngram_prob.items():
        if k.startswith(start_marker):
            next_keys.append(k)
            next_values.append(v)
    # Choose ngram according to its probability
    sentence = choices(next_keys, weights=next_values)[0]
    # Next ngram must start with the last word of this ngram
    last_word = sentence.rsplit(' ', 1)[1]
    
    # Keep generating sentences until we get an n-gram with an </s> end marker. 
    # Loop stops after the first </s>; we'll add the remanining markers later 
    end_marker = '</s>'
    while end_marker not in last_word:
        # Look for next ngram.
        next_keys = []
        next_values = []
        for k, v in ngram_prob.items():
            if k.startswith(last_word):
                next_keys.append(k)
                next_values.append(v)
        # Choose ngram. Add only its last word; the rest is already in sentence
        next_ngram = choices(next_keys, weights=next_values)[0]
        last_word = next_ngram.rsplit(' ', 1)[1]
        sentence += ' ' + last_word

    # Add missing sentence end markers
    sentence +=  (' ' + end_marker) * (n - 2)

    return sentence


test = ngram_prob(3, tokenize(example_text, punctuation=False, n = 3))
print(generate_sentence(test))
#print(sorted(test.items(), key=lambda x: x[1], reverse=False))
"""for i in range(1, n + 1):
ngram_counts_list.append(ngram_count(i, token_list))"""