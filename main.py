from game import ConnectFourGame, display_board
from ai import execute_random_move, human_player_move


def print_welcome():
    print("\n===== CONNECT 4 =====")
    print("1. Player vs Player")
    print("2. Player vs Computer")
    print("3. Computer vs Computer")
    print("4. Exit")
    print("====================")

if __name__ == "__main__":
    NUM_ROWS = 6
    NUM_COLS = 7

    while True:
        print_welcome()
        choice = input("Select game mode: ")
        
        if choice == "1":  # Player vs Player
            game = ConnectFourGame(human_player_move, human_player_move)
            # Override the original board printing to use our nicer display
            original_start = game.start
            def new_start(log_moves=True):
                game.state = game.state.__class__()
                while True:
                    display_board(game.state.board)
                    if game.state.player == 1:
                        game.player_1_ai(game)
                    else:
                        game.player_2_ai(game)
                    
                    if game.state.winner != -1:
                        display_board(game.state.board)
                        break
                
                if game.state.winner == 0:
                    print("End of game! Draw!")
                else:
                    print(f"End of game! Player {game.state.winner} wins!")
            
            game.start = new_start
            game.start()
            
        elif choice == "2":  # Player vs Computer
            # We'll implement this next
            print("Coming soon!")
            
        elif choice == "3":  # Computer vs Computer
            game = ConnectFourGame(execute_random_move, execute_random_move)
            game.run_n_matches(10, 120, True)
            
        elif choice == "4":  # Exit
            print("Thanks for playing!")
            break
            
        else:
            print("Invalid choice. Please try again.")