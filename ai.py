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