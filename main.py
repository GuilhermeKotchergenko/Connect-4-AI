from game import ConnectFourGame, display_board
from ai import execute_random_move, human_player_move, execute_smart_move


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
            # Ask if player wants to be Player 1 or Player 2
            player_choice = ""
            while player_choice not in ["1", "2"]:
                player_choice = input("Do you want to play as Player 1 (X) or Player 2 (O)? (1/2): ")
            
            if player_choice == "1":
                game = ConnectFourGame(human_player_move, execute_smart_move)
                player_symbol = "X"
                computer_symbol = "O"
            else:
                game = ConnectFourGame(execute_smart_move, human_player_move)
                player_symbol = "O"
                computer_symbol = "X"
            
            # Use the same display method as Player vs Player
            def new_start(log_moves=True):
                game.state = game.state.__class__()
                while True:
                    display_board(game.state.board)
                    
                    # Show whose turn it is
                    current_player = "Your" if ((game.state.player == 1 and player_choice == "1") or 
                                               (game.state.player == 2 and player_choice == "2")) else "Computer's"
                    print(f"\n{current_player} turn ({player_symbol if current_player == 'Your' else computer_symbol})")
                    
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
                    winner = "You" if ((game.state.winner == 1 and player_choice == "1") or 
                                       (game.state.winner == 2 and player_choice == "2")) else "Computer"
                    print(f"End of game! {winner} win!")
            
            game.start = new_start
            game.start()
            
        elif choice == "3":  # Computer vs Computer
            # Allow selecting different AI types
            print("\nSelect AI types:")
            print("1. Random vs Random")
            print("2. Smart vs Random")
            print("3. Smart vs Smart")
            ai_choice = input("Enter your choice (1-3): ")
            
            if ai_choice == "2":
                game = ConnectFourGame(execute_smart_move, execute_random_move)
            elif ai_choice == "3":
                game = ConnectFourGame(execute_smart_move, execute_smart_move)
            else:  # Default to random vs random
                game = ConnectFourGame(execute_random_move, execute_random_move)
                
            num_games = int(input("How many games to run? "))
            game.run_n_matches(num_games, 120, True)
            
        elif choice == "4":  # Exit
            print("Thanks for playing!")
            break
            
        else:
            print("Invalid choice. Please try again.")