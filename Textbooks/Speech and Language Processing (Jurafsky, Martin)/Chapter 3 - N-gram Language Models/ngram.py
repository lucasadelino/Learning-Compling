"""
Contains functions to build ngram language models
TODO: Remove extra whitespace when tokenize(punctuation==False)
TODO: Add unigram sentence generation
"""

import re
from random import choices
from math import log, exp 
from pathlib import Path

# Matches everything before a period, question mark, or exclamation mark. 
sentence_regex = re.compile(r'(\S(?:.+?)[\.\?!]+)')

# Matches either a sequence of word characters or a punctuation mark
token_regex = re.compile(r'(\w+|[“”":;\'-\.\?!,]+)')

# Matches punctuation marks
punctuation_regex = re.compile(r'([“”":;\'-\.\?!,]+)') 

# Matches en dashes surrounded by word characters. Useful for PT-BR parsing
travessao_regex = re.compile(r'(\w)-(\w)')

# Matches en dashes surrounded by word characters. Useful for PT-BR parsing
endmarker_regex = re.compile(r'</s>')

def sentence_segment(text):
    """Returns a list containing the argument text broken up into sentences. 
    Uses sentence_regex to look for sentences.
    """
    return list(sentence_regex.findall(text))

# TODO: Separate tokenizer into another file
def tokenize(text, punctuation = True, n=1):
    """
    A very crude tokenizer. Returns a list of tokens for each sentence in the 
    text passed as argument. Punctuation marks are considered tokens if 
    punctuation == True, or deleted if False. The n parameter adds n-1  
    sentence start <s> and end </s> markers to each sentence for ngram 
    processing. At present, this tokenizer doesn't  take named entities into 
    account or employs any normalization other than case folding.
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

    # Insert sentence start <s> and end </s> markers in each list of tokens
    if n > 1:
        for i, sentence in enumerate(token_list):
            token_list[i] = (['<s>'] * (n-1)) + sentence + (['</s>'] * (n-1))

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

def get_vocab_size(token_list):
    return len(ngram_count(1, token_list))

def get_token_count(token_list):
    """
    """
    token_count = 0
    for value in ngram_count(1, token_list).values():
        token_count += value

    return token_count

def ngram_prob(n, token_list):
    """
    Generates Maximum Likelihood Estimation probabilities of the ngrams present
    in a list of tokens. Returns a dictionary in which key-value pairs are,
    respectively, each ngram and its probability
    """    
    # This will contain the ngrams and their probabilities
    ngram_prob = {}

    # Get the counts of ngrams of the same n passed as argument
    ngrams =  ngram_count(n, token_list)
    # Get the count of lower-order ngram OR total number of tokens if n == 1
    if n > 1:
        lower_ngrams =  ngram_count(n - 1, token_list)
    elif n == 1:
        lower_ngram_count = get_token_count

    for key, count in ngrams.items():
        if n > 1:
            # Lower order ngram = current ngram minus its last word
            lower_ngram_key = key.rsplit(' ', 1)[0]
            lower_ngram_count = lower_ngrams[lower_ngram_key]
        ngram_prob.update({key: (count / lower_ngram_count)})
    
    return ngram_prob

def generate_sentence(ngram_probs):
    """
    Generates a sentence based on a dictionary of ngram probabilities.
    """
    # Look at keys in ngram_probs to figure out what's the order of our ngrams
    n = len(list(ngram_probs.keys())[0].split(' '))

    # Look for 1st ngram. Consider only ngrams that start with n-1 <s> markers
    next_keys = []
    next_values = []
    for k, v in ngram_probs.items():
        if k.startswith(('<s> ' * (n - 1)).rstrip()):
            next_keys.append(k)
            next_values.append(v)
    # Choose ngram according to its probability
    sentence = choices(next_keys, weights=next_values)[0]
    # Next ngram must start with the last word of this ngram
    last_word = sentence.rsplit(' ', 1)[1]
    
    # Keep generating sentences until we get an n-gram with an </s> end marker 
    # Loop stops after the first </s>; we'll add the remanining markers later 
    while '</s>' not in last_word:
        # Look for next ngram.
        next_keys = []
        next_values = []
        for k, v in ngram_probs.items():
            if k.startswith(last_word):
                next_keys.append(k)
                next_values.append(v)
        # Choose ngram. Don't add first word since it's already in the sentence
        next_ngram = choices(next_keys, weights=next_values)[0]
        sentence += ' ' + next_ngram.split(' ', 1)[1]
        last_word = next_ngram.rsplit(' ', 1)[1]

    # Add missing sentence end markers
    sentence +=  ' </s>' * ((n - 1) - len(endmarker_regex.findall(sentence)))

    return sentence

def perplexity(n, token_list):
    """
    Calculate the perplexity of a test set (broken down into a list of tokens)
    """
    # Collapse token list from a list of lists into a single list within list
    while len(token_list) > 1:
        for word in token_list[1]:
            token_list[0].append(word)
        token_list.pop(1)


    # Get the probability of the entire token list via chain rule of probs
    counts = ngram_count(n, token_list)
    probs = ngram_prob(n, token_list)
    log_prob = 0

    for k, v in counts.items():
        log_prob += v * log(probs.get(k))
    
    # Exclude </s> markers from total token count
    token_count = get_token_count
    if n > 1:
        token_count -= ngram_count(1, token_list).get('</s>')
    
    pp = exp(-(1/token_count) * log_prob)

    return pp

with open(Path.cwd() / 
'Textbooks' / 'Speech and Language Processing (Jurafsky, Martin)' / 
'Chapter 3 - N-gram Language Models' / 
'machado.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    tokenlist = tokenize(text, punctuation=True, n=5)
    #ngram_count(2, listie)
    print(perplexity(5, tokenlist))
    #sentence = ngram_prob(6, tokenize(text, punctuation=True, n=6))
    #print(generate_sentence(sentence))