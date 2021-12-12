import re

# Matches either a sequence of word characters or a punctuation mark
token_regex = re.compile(r'(\w+|[“”":;\'-\.\?!,]+)', re.UNICODE)

# Matches a sequence of alphabetic characters
word_regex = re.compile(r'(\w+)', re.UNICODE)

def tokenize(text, punctuation = True):
    """
    A very crude tokenizer. Returns a list of tokens for each sentence in the 
    text passed as argument. Punctuation marks are considered tokens if 
    punctuation == True, or deleted if False. At present, this tokenizer 
    doesn't take named entities into account or employ any normalization other 
    than case folding.
    """
    # This will contain a list for each sentence to be tokenized
    token_list = []
    
    for sentence in text:
        if punctuation == True:
            token_list.append(token_regex.findall(sentence))
        else:
            token_list.append(word_regex.findall(sentence))
    
    # Case fold all words to lowercase
    for each_list in token_list:
        for i, word in enumerate(each_list):
            if word.isupper() or word.istitle():
                each_list[i] = word.lower()

    return token_list