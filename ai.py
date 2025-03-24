import random

def execute_random_move(game):
    move = random.choice(game.state.available_moves)
    game.state = game.state.move(move)

def human_player_move(game):
    # Allow a human player to choose a move via console input
    while True:
        try:
            print(f"\nPlayer {game.state.player}'s turn")
            print(f"Available columns: {[col+1 for col in game.state.available_moves]}")
            column = int(input(f"Enter column number (1-{len(game.state.available_moves)}): ")) - 1  # Convert to 0-indexed

            
            if column in game.state.available_moves:
                game.state = game.state.move(column)
                break
            else:
                print("Invalid move! Column is full or out of range.")
        except ValueError:
            print("Please enter a number between 1 and {NUM_COLS}.")

# Aqui tem uma heuristica inventada pelo GPT, a ideia é modificar para MonteCarlo / Decision Tree
def execute_smart_move(game):
    """
    A smarter AI that evaluates potential moves and chooses the best one
    based on simple heuristics:
    1. If can win in one move, make that move
    2. If opponent can win in one move, block that move
    3. Prefer center columns
    4. Otherwise choose a move that maximizes potential winning lines
    """
    available_moves = game.state.available_moves
    current_player = game.state.player
    opponent = 3 - current_player  # In Connect 4, players are 1 and 2
    
    # Check if we can win in this move
    for move in available_moves:
        new_state = game.state.move(move)
        if new_state.winner == current_player:
            game.state = new_state
            return
    
    # Check if opponent would win in their next move and block it
    for move in available_moves:
        # Simulate opponent playing in this position
        test_state = game.state.move(move)
        opponent_state = test_state
        opponent_state.player = opponent  # Change player for evaluation
        
        for opponent_move in opponent_state.available_moves:
            if opponent_move == move:  # Skip the move we just made in simulation
                continue
            potential_state = opponent_state.move(opponent_move)
            if potential_state.winner == opponent:
                # Found a move where opponent could win next turn, block it
                game.state = game.state.move(move)
                return
    
    # Evaluate all potential moves
    best_move = None
    best_score = float('-inf')
    
    for move in available_moves:
        new_state = game.state.move(move)
        # Score the move based on:
        # - Number of potential winning lines (3 in a row with empty space)
        # - Central position control
        score = (new_state.count_lines(3, current_player) * 10 + 
                 new_state.central(current_player) * 2 - 
                 new_state.count_lines(3, opponent) * 8)
        
        if score > best_score:
            best_score = score
            best_move = move
    
    # If still no good move found, prefer central columns
    if best_move is None:
        for preferred in [3, 2, 4, 1, 5, 0, 6]:  # Preference order (center to edges)
            if preferred in available_moves:
                best_move = preferred
                break
    
    # Make the best move
    game.state = game.state.move(best_move)