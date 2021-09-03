#TODO: Augment the minimum edit distance algorithm to output an alignment; you will need to store pointers and add a stage to compute the backtrace

DEL_COST = 1
INS_COST = 1
SUB_COST_DIF = 2
SUB_COST_EQL = 0

def min_edit_dist(source, target):
    
    n = len(source)
    m = len(target)
    matrix = [[0] * (len(target) + 1) for _ in range(len(source) + 1)]
    # Initialization: the zeroth row and column is the distance from the empty string
    for i in range(1, n + 1):
        matrix[i][0] = matrix[i-1][0] + DEL_COST
    for j in range(1, m + 1):
        matrix[0][j] = matrix[0][j-1] + INS_COST

    # Recurrence relation:
    for i in range(0, n):
        for j in range(0, m):
            sub_cost = 0
            if source[i] == target[j]: #Check if we're subbing different or identical
                sub_cost = SUB_COST_EQL
            else:
                sub_cost = SUB_COST_DIF
            matrix[i+1][j+1] = min(matrix[i][j+1] + DEL_COST, matrix[i][j] + sub_cost ,matrix[i+1][j] + INS_COST)

    return matrix[n][m]