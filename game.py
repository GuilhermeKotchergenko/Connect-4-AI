import time
from config import NUM_ROWS, NUM_COLS
from state import State


def display_board(board):
        #Print the Connect 4 board in a readable format
        print("\n  1 2 3 4 5 6 7")  # Column numbers
        print(" ---------------")
        for row in board:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print(" ", end="|")
                elif cell == 1:
                    print("X", end="|")
                elif cell == 2:
                    print("O", end="|")
            print()
        print(" ---------------")


class ConnectFourGame:
    def __init__(self, player_1_ai, player_2_ai):
        self.state = State() # initial state
        self.player_1_ai = player_1_ai # store player 1 type (move selection method)
        self.player_2_ai = player_2_ai # store player 2 type (move selection method)
        
    def start(self, log_moves = False):
        self.state = State()
        while True:
            # play the move
            if self.state.player == 1:
                self.player_1_ai(self)
            else:
                self.player_2_ai(self)          
            if log_moves:
                print(self.state.board)
            
            # check the winner and end the game if so
            if self.state.winner != -1:
                break
        # print the winner of the game
        if self.state.winner == 0:
            print("End of game! Draw!")
        else:
            print(f"End of game! Player {self.state.winner} wins!")
    
    def run_n_matches(self, n, max_time = 3600, log_moves = False):
        # utility function to automate n matches execution
        # should return the total distribution of players wins and draws
        start_time = time.time()
        
        results = [0, 0, 0] # [draws, player 1 victories, player 2 victories]
        
        while n > 0 and time.time() - start_time < max_time:
            n -= 1
            self.start(log_moves)
            results[self.state.winner] += 1
            
        print("\n=== Elapsed time: %s seconds ===" % (int(time.time() - start_time)))
        print(f"  Player 1: {results[1]} victories")
        print(f"  Player 2: {results[2]} victories")
        print(f"  Draws: {results[0]} ")
        print("===============================")

