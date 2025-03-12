from game import ConnectFourGame
from ai import execute_random_move

if __name__ == "__main__":
    game = ConnectFourGame(execute_random_move, execute_random_move)
    game.run_n_matches(10, 120, False)