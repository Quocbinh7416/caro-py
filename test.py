import math


# Minimax function with Alpha-Beta Pruning
def minimax(depth, node_index, maximizing_player, values, alpha, beta):
    # Base case: leaf node is reached
    if depth == 3:  # Assume depth 3 is the bottom of the tree
        return values[node_index]

    if maximizing_player:
        max_eval = -math.inf
        for i in range(2):  # Each node has 2 children
            eval = minimax(depth + 1, node_index * 2 + i, False, values, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval

    else:  # Minimizing player
        min_eval = math.inf
        for i in range(2):
            eval = minimax(depth + 1, node_index * 2 + i, True, values, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval


# Example game tree with leaf node values (depth 3 binary tree)
values = [3, 5, 6, 9, 1, 2, 0, -1]

# Starting the minimax algorithm (depth 0, node 0, maximizing player)
optimal_value = minimax(0, 0, True, values, -math.inf, math.inf)

print(f"Optimal value: {optimal_value}")
