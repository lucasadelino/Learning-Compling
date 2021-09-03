DEL_COST = 1
INS_COST = 1
SUB_COST_DIF = 1
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
    for i in range(1, n):
        for j in range(1, m):
            sub_cost = 0
            if source[i] == target[j]:
                sub_cost = SUB_COST_EQL
            else:
                sub_cost = SUB_COST_DIF
            matrix[i][j] = min(matrix[i-1][j] + DEL_COST, matrix[i-1][j-1] + sub_cost ,matrix[i][j-1] + INS_COST)

    return matrix[n][m]

print(min_edit_dist('leda', 'deal'))