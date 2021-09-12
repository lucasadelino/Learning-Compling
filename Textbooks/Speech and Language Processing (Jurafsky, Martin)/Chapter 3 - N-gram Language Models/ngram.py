"""
Contains functions to build ngram language models
TODO: Create ngram probability function
"""

import re
from copy import copy

# Matches everything before a period, question mark, or exclamation mark. 
sentence_regex = re.compile(r'(\S(?:.+?)[\.\?!])')

# Matches either a sequence of word characters or a punctuation mark
token_regex = re.compile(r'(<?\w+>?|[“”":;\'-\.\?!,])')

# Matches punctuation marks
punctuation_regex = re.compile(r'([“”":;\'-\.\?!,])') 

# Matches en dashes surrounded by word characters. Useful for PT-BR parsing
travessao_regex = re.compile(r'(\w)-(\w)')

# TODO: Read example text from a .txt file
example_text = 'Vivo só, com um criado. A casa em que moro é própria; fi-la construir de propósito, levado de um desejo tão particular que me vexa imprimi-lo, mas vá lá. Um dia, há bastantes anos, lembrou-me reproduzir no Engenho Novo a casa em que me criei na antiga rua de Matacavalos, dando-lhe o mesmo aspecto e economia daquela outra, que desapareceu. Construtor e pintor entenderam bem as indicações que lhes fiz: é o mesmo prédio assobradado, três janelas de frente, varanda ao fundo, as mesmas alcovas e salas. Na principal destas, a pintura do teto e das paredes é mais ou menos igual, umas grinaldas de flores miúdas e grandes pássaros que as tomam nos bicos, de espaço a espaço. Nos quatro cantos do teto as figuras das estações, e ao centro das paredes os medalhões de César, Augusto, Nero e Massinissa, com os nomes por baixo... Não alcanço a razão de tais personagens. Quando fomos para a casa de Matacavalos, já ela estava assim decorada; vinha do decênio anterior. Naturalmente era gosto do tempo meter sabor clássico e figuras antigas em pinturas americanas. O mais é também análogo e parecido. Tenho chacarinha, flores, legume, uma casuarina, um poço e lavadouro. Uso louça velha e mobília velha. Enfim, agora, como outrora, há aqui o mesmo contraste da vida interior, que é pacata, com a exterior, que é ruidosa.'

def sentence_segment(text):
    """Returns a list containing the argument text broken up into sentences. 
    Uses sentence_regex to look for sentences."""
    return list(sentence_regex.findall(text))

# TODO: Separate tokenizer into another file
def tokenize(text, punctuation = True):
    """
    A very crude tokenizer. Returns a list of tokens for each sentence in the 
    text passed as argument. Punctuation marks are considered tokens if the 
    'punctuation' argument is set to True, or deleted if punctuation is set to 
    False. At present, this tokenizer doesn't take named entities into account,
    or employs any normalization other than case folding.
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

    return token_list

def ngram_count(n, token_list):
    """
    Counts the ngrams in a list of tokens. Returns a dictionary containing each
    ngram and their frequency counts.
    """

    # We'll need to use n - 1 several times (e.g. a bigram requires 1 each of 
    # <s> and </s>, a trigram requires 2, etc.), so we'll call it 'm'
    m = n - 1

    token_list_copy = copy(token_list)
    
    # Insert sentence start <s> and end </s> markers into each list of tokens
    for i, sentence in enumerate(token_list_copy):
        token_list_copy[i] = (['<s>'] * m) + sentence + (['</s>'] * m)

    ngram_dict = {}

    for sentence in token_list_copy:
        for i in range(m, len(sentence)):
            # Point at last (i - m) words for concatenation
            pointer = i - m
            # Form an ngram by concatenating last (i - m) words, up to i
            ngram = ''
            while pointer <= i: 
                ngram += sentence[pointer] + ' '
                pointer += 1
            # Strip whitespaces and add ngram to dict
            ngram = ngram.rstrip()
            ngram_dict.setdefault(ngram, 0)
            ngram_dict[ngram] += 1
    
    return ngram_dict

test = ngram_count(2, tokenize(example_text, punctuation=False))
print(sorted(test.items(), key=lambda x: x[1], reverse=True))