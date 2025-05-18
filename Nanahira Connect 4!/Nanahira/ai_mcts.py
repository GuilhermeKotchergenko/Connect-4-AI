import random
import math
from copy import deepcopy
from multiprocessing import Pool
from .ai_id3 import State, NUM_COLS
import numpy as np
from numba import njit
import time

class MCNode:
    def __init__(self, state: State, player: int):
        self.state   = state
        self.player  = player
        self.wins    = 0
        self.visits  = 0
        self.children = []
        self.is_terminal = (state.winner != -1)

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, player):
        if self.is_terminal:
            return None
        for move in self.state.available_moves:
            new_state = self.state.move(move)
            self.children.append(MCNode(new_state, player))
        return random.choice(self.children)

    def update_stats(self, value):
        reward = 1 if self.player == value else 0
        self.wins += reward
        self.visits += 1

class MCTree:
    def __init__(self, root):
        self.root = root

    def expand(self, node, player_cur):
        return node.add_child(player_cur)

def select(node, children, c, player):
    for child in children:
        if child.visits == 0:
            return child
    best_value = -math.inf
    best_node  = None
    ln_parent  = math.log(node.visits)
    for child in children:
        uct = (child.wins / child.visits) + c * math.sqrt(ln_parent / child.visits)
        if uct > best_value:
            best_value, best_node = uct, child
    return best_node

def roll_out(node):
    st = node.state
    flat = np.array([cell for row in st.board for cell in row], dtype=np.int8)
    heights = np.array([r for r in st.column_heights], dtype=np.int8)
    try:
        return numba_rollout(flat, heights, st.player)
    except Exception as e:
        print(f"⚠️ Numba rollout failed: {e}")
        return st.simulate_random_game()

def best_action(root):
    return max(root.children, key=lambda child: child.wins / child.visits)

def monte_carlo(epochs, tree, c, player):
    for _ in range(epochs):
        visited = []
        player_cur = player
        node = tree.root
        visited.append(node)

        while not node.is_leaf() and not node.is_terminal:
            node = select(node, node.children, c, player_cur)
            visited.append(node)
            player_cur = 3 - player_cur

        new_child = tree.expand(node, player_cur)
        if new_child is not None and not new_child.is_terminal:
            visited.append(new_child)
            value = roll_out(new_child)
        else:
            value = node.state.winner if node.is_terminal else roll_out(node)

        for n in visited:
            n.update_stats(value)

    return best_action(tree.root)

def execute_monte_carlo_move(epochs, c, player):
    def inner(game):
        root = MCNode(deepcopy(game.state), 3 - player)
        best_node = monte_carlo(epochs, MCTree(root), c, player)
        for col in range(NUM_COLS):
            if game.state.column_heights[col] != best_node.state.column_heights[col]:
                return col
        return random.choice(game.state.available_moves)
    return inner

def mcts_worker(args):
    (root_state, epochs, c, player) = args
    tree = MCTree(MCNode(deepcopy(root_state), player))
    monte_carlo(epochs, tree, c, player)
    stats = [(child.wins, child.visits) for child in tree.root.children]
    return stats

def execute_monte_carlo_move_parallel(epochs, c, player, workers=4):
    def inner(game):
        root_state = game.state
        root = MCNode(deepcopy(root_state), player)

        for mv in root_state.available_moves:
            root.children.append(MCNode(root_state.move(mv), 3-player))

        per_worker = epochs // workers
        args = [(root_state, per_worker, c, player) for _ in range(workers)]

        with Pool(workers) as pool:
            results = pool.map(mcts_worker, args)

        num_moves = len(root.children)
        agg_wins   = [0.0]*num_moves
        agg_visits = [0]*num_moves
        for stats in results:
            for i, (w,v) in enumerate(stats):
                agg_wins[i]   += w
                agg_visits[i] += v

        best_idx = max(
            range(num_moves),
            key=lambda i: (agg_wins[i]/agg_visits[i]) if agg_visits[i] > 0 else -1
        )
        best_child = root.children[best_idx]

        for col in range(NUM_COLS):
            if root_state.column_heights[col] != best_child.state.column_heights[col]:
                return col
        return random.choice(root_state.available_moves)
    return inner

@njit
def numba_rollout(flat_board, heights, player):
    board = flat_board.copy()
    available = [i for i in range(7) if heights[i] >= 0]
    column_heights = heights.copy()
    
    def check_win(board, p):
        for r in range(6):
            for c in range(7):
                idx = r * 7 + c
                # Horizontal
                if c <= 3:
                    won = True
                    for i in range(4):
                        if board[idx + i] != p:
                            won = False
                            break
                    if won:
                        return True
                # Vertical
                if r <= 2:
                    won = True
                    for i in range(4):
                        if board[idx + i*7] != p:
                            won = False
                            break
                    if won:
                        return True
                # Diagonal /
                if c <= 3 and r <= 2:
                    won = True
                    for i in range(4):
                        if board[idx + i*8] != p:
                            won = False
                            break
                    if won:
                        return True
                # Diagonal \
                if c >= 3 and r <= 2:
                    won = True
                    for i in range(4):
                        if board[idx + i*6] != p:
                            won = False
                            break
                    if won:
                        return True
        return False

    while True:
        if not available:
            return 0  # Tie

        mv_idx = np.random.randint(len(available))
        col = available[mv_idx]
        row = column_heights[col]
        board[row * 7 + col] = player
        column_heights[col] -= 1
        if column_heights[col] < 0:
            available.remove(col)

        if check_win(board, player):
            return player

        player = 3 - player

def benchmark_mcts(epochs=1000, mode="normal", parallel_workers=4):
    dummy_state = State()
    dummy_state.board = [[0]*7 for _ in range(6)]
    dummy_state.column_heights = [5]*7
    dummy_state.available_moves = list(range(7))
    dummy_state.player = 1

    class DummyGame:
        def __init__(self, state):
            self.state = state

    if mode == "normal":
        ai_func = execute_monte_carlo_move(epochs, c=1.4, player=1)
    elif mode == "parallel":
        ai_func = execute_monte_carlo_move_parallel(epochs, c=1.4, player=1, workers=parallel_workers)
    else:
        print("Unknown mode:", mode)
        return

    print(f"Benchmarking MCTS ({mode}) with {epochs} simulations...")

    start = time.time()
    move = ai_func(DummyGame(dummy_state))
    duration = time.time() - start

    sims_per_sec = epochs / duration
    print(f"Best move: {move}")
    print(f"Total time: {duration:.4f}s")
    print(f"Simulations/sec: {sims_per_sec:.2f}")
    return duration, sims_per_sec, move