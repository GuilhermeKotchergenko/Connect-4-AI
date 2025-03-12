from copy import deepcopy
from config import NUM_ROWS, NUM_COLS



class State:
    def __init__(self):
        # initialize the board info here and any additional variables
        self.board = [[0]*NUM_COLS for i in range(NUM_ROWS)] # [[0,0,0,...], [0,0,0,...], ...] board initial state (all zeros)
        self.column_heights = [NUM_ROWS - 1] * NUM_COLS # [5, 5, 5, 5, 5, 5, 5] useful to keep track of the index in which pieces should be inserted
        self.available_moves = list(range(7)) # [0, 1, ..., 6] list of playable columns (not full)
        self.player = 1
        self.winner = -1 # -1 - no winner (during game); 0 - draw; 1- player 1; 2 - player 2
        
    #--------------------------------------------------#
    def check_line(self, n, player, values):
        num_pieces = sum(list(map(lambda val: val == player, values)))
        # code above is equivalent to
        # num_pieces = 0
        # for val in values:
        #     if val == player:
        #         num_pieces += 1
        if n == 4:
            return num_pieces == 4
        if n == 3:
            num_empty_spaces = sum(list(map(lambda val: val == 0, values)))
            return num_pieces == 3 and num_empty_spaces == 1
    
    # calculates the number of lines with 4 pieces (horizontal, vertical, diagonal) of a given player.
    # calculates the number of sets of 4 consecutive spots that have three pieces of the player followed by an empty spot, i.e., that are possibilities to win the game.
    def count_lines(self, n, player):
        num_lines = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # checks vertical line
                if col < NUM_COLS - 3 and self.check_line(n, player, [self.board[row][col], self.board[row][col+1], self.board[row][col+2], self.board[row][col+3]]):
                    num_lines += 1
                # checks horizontal line
                if row < NUM_ROWS - 3 and self.check_line(n, player, [self.board[row][col], self.board[row+1][col], self.board[row+2][col], self.board[row+3][col]]):
                    num_lines += 1
                # checks upper diagonal line
                if row < NUM_ROWS - 3 and col < NUM_COLS - 3 and self.check_line(n, player, [self.board[row][col], self.board[row+1][col+1], self.board[row+2][col+2], self.board[row+3][col+3]]):
                    num_lines += 1
                # checks lower diagonal line
                if row < NUM_ROWS - 3 and col > 3 and self.check_line(n, player, [self.board[row][col], self.board[row+1][col-1], self.board[row+2][col-2], self.board[row+3][col-3]]):
                    num_lines += 1
        return num_lines
    
    # assigns 2 points to each player piece in the center column of the board (column 4) and 1 point to each piece in the columns around it (columns 3 and 5).
    def central(self, player):
        points = 0
        for row in range(NUM_ROWS):
            if self.board[row][4] == player: # center column
                points += 2  
            if self.board[row][3] == player: # around center column
                points += 1 
            if self.board[row][5] == player: # around center column
                points += 1
        return points
    #--------------------------------------------------#
        
    
        
    def move(self, column): 
        # function that performs a move given the column number and returns the new state
        #--------------------------------------------------#
        state_copy = deepcopy(self)
        
        height = state_copy.column_heights[column]
        state_copy.column_heights[column] = height
        state_copy.board[height][column] = self.player
        
        if height == 0:
            state_copy.available_moves.remove(column)
        else:
            state_copy.column_heights[column] = height - 1
        
        state_copy.update_winner() 
        state_copy.player = 3 - self.player # update player turn
        
        return state_copy

    def update_winner(self):
        if self.count_lines(4, 1) > 0:
            self.winner = 1
        elif self.count_lines(4, 2) > 0:
            self.winner = 2
        elif len(self.available_moves) == 0:
            self.winner = 0