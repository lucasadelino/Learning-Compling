#TODO: Implement pretty print matrix. Options for outputting raw text or LaTeX
#TODO: Implement weighting  

from random import choice

DEL_COST = 1
INS_COST = 1
SUB_COST_DIF = 2
SUB_COST_EQL = 0

def min_edit_dist(source, target):
    """
    Calculate the edit distance between source and target strings. Returns a 
    tuple containing:
        The minimum edit distance [0]
        The dynamic programming matrix used to calculate the above [1] 
    """

    n, m = (len(source), len(target))
    
    # Initialize empty matrix. Each entry is a dict containing: 
        # The cell value
        # A list of pointers
    matrix = [[{'value': 0, 'pointers': []} for _ in range(len(target) + 1)] for _ in range(len(source) + 1)]
    
    # Fill base cases' values and pointers
    for i in range(1, n + 1):
        matrix[i][0]['value'] = matrix[i-1][0]['value'] + DEL_COST
        matrix[i][0]['pointers'].append('up')
    for j in range(1, m + 1):
        matrix[0][j]['value'] = matrix[0][j-1]['value'] + INS_COST
        matrix[0][j]['pointers'].append('left')

    # Recursively populate matrix:
    for i in range(0, n):
        for j in range(0, m):
            sub_cost = 0
            
            # Check if subbing for a different or identical character
            if source[i] == target[j]: 
                sub_cost = SUB_COST_EQL
            else:
                sub_cost = SUB_COST_DIF
            
            # Get neighboring cell values
            up_value = matrix[i][j+1]['value'] + DEL_COST 
            diag_value = matrix[i][j]['value'] + sub_cost 
            left_value = matrix[i+1][j]['value'] + INS_COST

            # Set current cell value
            min_value = min(up_value, diag_value, left_value)
            matrix[i+1][j+1]['value'] = min_value
            
            # Set pointers
            if up_value == min_value:
                matrix[i+1][j+1]['pointers'].append('up')
            if diag_value == min_value:
                matrix[i+1][j+1]['pointers'].append('diag')
            if left_value == min_value:
                matrix[i+1][j+1]['pointers'].append('left')

    return (matrix[n][m]['value'], matrix)
    
def align(source, target):
    """
    Generates an alignment by backtracing the dynamic programming matrix of the 
    edit distance between source and target strings. When backtracing, if 
    multiple directions are avaliable, chooses a random direction.  Returns a 
    tuple containing:
        The source word's output [0]
        The target word's output [1]
        The operations performed to align source with target [2]
    """
    source_output = ''
    target_output = ''
    commands = ''

    matrix = min_edit_dist(source, target)[1]
    
    # Start from last value in matrix
    i, j = len(matrix) - 1, len(matrix[0]) - 1
    while i + j > 0:
        current_cell = matrix[i][j]
        direction = current_cell['pointers']
        
        # If there are multiple pointers, randomly choose one
        if len(direction) > 1:
            direction = choice(direction)
        # If there's only one pointer, transform it into a string
        else:
            direction = direction[0] 
        
        # Backtrace and generate alignment output based on pointer
        if direction == 'up':
            i -= 1
            source_output = source[i] + source_output 
            target_output = '*' + target_output
            commands = 'd' + commands
        if direction == 'diag':
            i -= 1
            j -= 1
            source_output = source[i] + source_output 
            target_output = target[j] + target_output
            if source[i] == target[j]:
                commands = ' ' + commands
            else:
                commands = 's' + commands
        if direction == 'left':
            j -= 1
            source_output = '*' + source_output
            target_output = target[j] + target_output
            commands = 'i' + commands

    return (source_output, target_output, commands)

def pprint_alignment(alignment):
    """Pretty prints an alignment"""
    for list in alignment:
        for character in list:
            print(character, end=' ')
        print()

#def pprint_min_edit_dist(source, target): 
    #TODO
    