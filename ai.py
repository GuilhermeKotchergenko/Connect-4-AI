import random

def execute_random_move(game):
    move = random.choice(game.state.available_moves)
    game.state = game.state.move(move)