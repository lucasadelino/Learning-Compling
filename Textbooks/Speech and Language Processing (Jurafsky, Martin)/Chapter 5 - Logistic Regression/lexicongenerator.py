from pathlib import Path

with open(Path.cwd() / 'oplexicon.txt', 'r') as file:
    contents = file.read().splitlines()
    positivos = ''
    negativos = ''
    for string in contents:
        # This classifier doesnt support lemmatization, so we ignore any words
        # with spaces in them (most of them expressions/idioms using infinitive
        # verbs)
        if ' ' in string.split('.')[0]:
            continue
        # Ignore words with neutral polarity
        if string.split('=')[-1] == '0':
            continue
        
        # If polarity is negative
        if string.split('=')[-1] == '-1':
            negativos += string.split('.')[0] + '\n'
        # If polarity is negative
        else:
            positivos += string.split('.')[0] + '\n'

    with open(Path.cwd() / 'negativos.txt', 'w') as postxt:
        postxt.write(negativos)

    with open(Path.cwd() / 'positivos.txt', 'w') as negtxt:
        negtxt.write(positivos)


    

