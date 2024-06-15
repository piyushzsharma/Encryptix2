import math

# Constants for the game
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

# Initialize the board
def create_board():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Print the board
def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Check for a win
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

# Check for a draw
def is_draw(board):
    return all([cell != EMPTY for row in board for cell in row])

# Get available moves
def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, AI):
        return 1
    if check_winner(board, PLAYER):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = AI
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[r][c] = EMPTY
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = PLAYER
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[r][c] = EMPTY
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Find the best move
def find_best_move(board):
    best_move = None
    best_value = -math.inf
    for (r, c) in get_available_moves(board):
        board[r][c] = AI
        move_value = minimax(board, 0, False, -math.inf, math.inf)
        board[r][c] = EMPTY
        if move_value > best_value:
            best_value = move_value
            best_move = (r, c)
    return best_move

# Main game loop
def play_game():
    board = create_board()
    current_player = PLAYER
    
    while True:
        print_board(board)
        
        if current_player == PLAYER:
            move = None
            while move not in get_available_moves(board):
                try:
                    move = tuple(map(int, input("Enter your move (row col): ").split()))
                except ValueError:
                    print("Invalid input. Enter row and column as numbers.")
            board[move[0]][move[1]] = PLAYER
        else:
            print("AI is making a move...")
            move = find_best_move(board)
            board[move[0]][move[1]] = AI
        
        if check_winner(board, current_player):
            print_board(board)
            print(f"{current_player} wins!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = AI if current_player == PLAYER else PLAYER

# Start the game
if __name__ == "__main__":
    play_game()
