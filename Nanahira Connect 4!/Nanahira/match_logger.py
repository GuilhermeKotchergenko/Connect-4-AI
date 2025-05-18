import csv
import os

def log_match_step(state, player, ai_type, move, winner=None, log_path="match_log.csv"):
    flat_board = [cell for row in state.board for cell in row]
    row = {f"cell_{i}": flat_board[i] for i in range(len(flat_board))}
    row.update({
        "player": player,
        "ai_type": ai_type,
        "mtcarlomove": move,
        "winner": winner if winner is not None else ""
    })

    file_exists = os.path.exists(log_path)
    with open(log_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)