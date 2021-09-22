""" 
This is a very basic chatbot that uses regexes to look for patterns and come up
with responses. In its current state, it's very easy to exhaust or confuse the 
bot. While it's always possible to add more patterns to cover more cases, 
by design this program lacks the sophistication or ease of extensibility of an 
ELIZA-like chatbot.   
"""

import re

# This list contains possible patterns, their substitutions, and their ranks.
# See template at the end of list
pattern_dict = [
{'pattern': r'.*h(i|ello).*', 
 'response': "Hello there. How are you feeling today?", 
 'rank': 3},
{'pattern': r'.*(bro(ther)?|sis(ter)?|mother|m(o|u)m|m(a|om)ma|father|dad(dy)?|husband|wife).*', 
 'response': r'Tell me more about your \1.', 
 'rank': 5},
{'pattern': r".*i(?:'|\sa)m.*(sad|down|depressed|upset|blue|miserable|tired|exhausted|pooped).*", 
 'response': r'Why do you feel \1?', 
 'rank': 4},
{'pattern': r".*ph(?:\.)?d(?:\.)?.*", 
 'response': "Intellectual work can be very draining. Don't beat yourself up.", 
 'rank': 3},
{'pattern': r".*i(?:'|\sa)m.*(happy|g(?:ood|reat)).*", 
 'response': r"I'm glad to hear that you're \1. Anything else you'd like to talk about?", 
 'rank': 3},
{'pattern': r".*?(s?he)(?:'|\si)s.*", 
 'response': r"Do you wish that \1 was different?", 
 'rank': 2},
{'pattern': r".*(a lot of |too much )?work(?:ing)?( a lot| too much)?.*", 
 'response': "It's good to take a break now and then", 
 'rank': 5}
#{'pattern': r"", 
# 'response': r"", 
# 'rank': 0},
]

print('Hello.')
# Main program loop
while True:
    user_input = input()
    highest_rank = 0
    chosen_pattern = {}
    # Look for match in pattern_dict
    for item in pattern_dict:
        this_regex = re.compile(item['pattern'], re.I)
        if this_regex.search(user_input) is not None:
            # Check if current match is the highest-ranked possible 
            if item['rank'] > highest_rank:
                highest_rank = item['rank']
                chosen_pattern = item
    # If something matches
    if len(chosen_pattern) != 0:
        chosen_regex = re.compile(chosen_pattern['pattern'], re.I)
        print(chosen_regex.sub(chosen_pattern['response'], user_input))
    # If nothing matches
    else:
        print('Tell me more about that.')
