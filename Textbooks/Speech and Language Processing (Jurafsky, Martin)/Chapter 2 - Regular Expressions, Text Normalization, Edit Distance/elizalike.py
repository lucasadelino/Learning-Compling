"""
This was my first try at building an ELIZA-like chatbot. I began by reading 
Weizenbaum's 1966 article, which details the structure of the original ELIZA. 
My first impulse was to see if I could replicate that structure while leaving 
out the script. It very quickly became apparent why a script was necessary in 
the first place. The complexity of ELIZA's keyword dictionary, with its nested 
lists, is what lends that the program its remarkable extensibility. It also 
makes it extremely difficult for someone to write the dictionary by hand, 
wihtout a separate script. 

Writing an ELIZA-like program with an extensible script, however, seems way
beyond what exercise 2.3 in the textbook asks for. I may be wrong, but the 
impression I got from the prompt was that this was supposed to be a simpler
program, one made mainly to practice regex substitutions. I will try that 
first (check out myfirstchatbot.py). When I'm done, however, I intend to come 
back to this program and flesh it out as much as I can. 

TODO: Add a .txt script to ELIZA. 
      Add parser to read .txt and load it into keyword_list
      Ask friends to talk to ELIZA and build the script based on their input
TODO: Add function that stores words encountered for the first time in a .txt
"""

import re

""" Keyword entry data structure:
    {'keyword': '', 'rank': 0, 'decomp_list': ({'decomp_rule': '', 'recomp_list': ({'recomp_rule': '', 'times_used': 0})})}"""
    
keyword_list = [
{'keyword': r'[Hh](i|ello)', 'rank': 3, 'decomp_list': [{'decomp_rule': r'.*', 'recomp_list': [{'recomp_rule': 'Hello there', 'times_used': 0}]}]}
]

while True:
    user_input = input()
    for k_list_item in keyword_list:
        key_match = re.compile(k_list_item['keyword'])
        if key_match is not None: 
            for d_list_item in k_list_item['decomp_list']:
                decomp_match = re.compile(d_list_item['decomp_rule'])
                if decomp_match is not None:
                    min_times_used = d_list_item['recomp_list'][0]['times_used']
                    for r_list_item in d_list_item['recomp_list']:
                        if r_list_item['times_used'] <= min_times_used:
                            print(r_list_item['recomp_rule'])
                            r_list_item['times_used'] += 1
            break