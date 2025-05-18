import pandas as pd
import random
import numpy as np
from copy import deepcopy
from collections import Counter
import time
import math
import os
import hashlib
import joblib
from concurrent.futures import ProcessPoolExecutor

NUM_ROWS = 6
NUM_COLS = 7

learned_trees_p1 = None
learned_trees_p2 = None

# Difficulty configuration for training and AI behavior
ID3_DIFFICULTY_CONFIG = {
    "Easy": {"n_trees": 3, "max_depth": 5},
    "Medium": {"n_trees": 5, "max_depth": 7},
    "Hard": {"n_trees": 7, "max_depth": 9},
}

def compute_file_hash(filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    return hashlib.md5(file_data).hexdigest()

def hash_board(rec):
    board_vals = ''.join(str(int(rec[f'cell_{i}'])) for i in range(42))
    return hashlib.md5(board_vals.encode()).hexdigest()

class ID3DecisionTree:
    def __init__(self):
        self.tree = None

    def fit(self, X: pd.DataFrame, y: pd.Series, max_depth=None):
        data = X.copy()
        data['label'] = y
        self.tree = self._id3(data, X.columns, depth=0, max_depth=max_depth)

    def _entropy(self, labels):
        counts = Counter(labels)
        total = len(labels)
        entropy = 0
        for count in counts.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        return entropy

    def _information_gain(self, data, feature, target_attribute='label'):
        total_entropy = self._entropy(data[target_attribute])
        values = data[feature].unique()
        weighted_entropy = 0
        for value in values:
            subset = data[data[feature] == value]
            weighted_entropy += (len(subset) / len(data)) * self._entropy(subset[target_attribute])
        return total_entropy - weighted_entropy

    def _id3(self, data, features, depth=0, max_depth=None):
        labels = data['label']
        if len(set(labels)) == 1:
            return DecisionNode(label=labels.iloc[0])
        if len(features) == 0 or (max_depth is not None and depth >= max_depth):
            return DecisionNode(label=labels.mode()[0])

        gains = [(feature, self._information_gain(data, feature)) for feature in features]
        best_feature, _ = max(gains, key=lambda item: item[1])
        node = DecisionNode(feature=best_feature)

        for value in data[best_feature].unique():
            subset = data[data[best_feature] == value]
            if subset.empty:
                node.children[value] = DecisionNode(label=labels.mode()[0])
            else:
                remaining_features = features.drop(best_feature)
                node.children[value] = self._id3(subset, remaining_features, depth + 1, max_depth)
        return node

    def predict_one(self, example, node=None):
        if node is None:
            node = self.tree
        if node.is_leaf():
            return node.label
        feature_value = example[node.feature]
        child = node.children.get(feature_value)
        if child is None:
            return None
        return self.predict_one(example, child)

    def predict(self, X: pd.DataFrame):
        return X.apply(lambda row: self.predict_one(row), axis=1)

class DecisionNode:
    def __init__(self, feature=None, children=None, label=None):
        self.feature = feature
        self.children = children if children is not None else {}
        self.label = label

    def is_leaf(self):
        return self.label is not None

class State:
    def __init__(self):
        self.board = [[0]*NUM_COLS for _ in range(NUM_ROWS)]
        self.column_heights = [NUM_ROWS - 1] * NUM_COLS
        self.available_moves = list(range(NUM_COLS))
        self.player = 1
        self.winner = -1

        def simulate_random_game(self):
            # Create a shallow fast simulation copy
            state = State()
            state.board = [row[:] for row in self.board]
            state.player = self.player
            state.column_heights = self.column_heights[:]
            state.available_moves = self.available_moves[:]
            state.winner = self.winner

            while state.winner == -1:
                move = random.choice(state.available_moves)

                row = state.column_heights[move]
                state.board[row][move] = state.player

                if row == 0:
                    state.available_moves.remove(move)
                else:
                    state.column_heights[move] -= 1

                # Check winner directly
                state.update_winner()
                state.player = 3 - state.player

            return state.winner


    def check_line(self, n, player, values):
        num_pieces = sum(val == player for val in values)
        if n == 4:
            return num_pieces == 4
        if n == 3:
            return num_pieces == 3 and values.count(0) == 1

    def count_lines(self, n, player):
        num_lines = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if col < NUM_COLS - 3 and self.check_line(n, player, [self.board[row][col+i] for i in range(4)]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and self.check_line(n, player, [self.board[row+i][col] for i in range(4)]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and col < NUM_COLS - 3 and self.check_line(n, player, [self.board[row+i][col+i] for i in range(4)]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and col > 2 and self.check_line(n, player, [self.board[row+i][col-i] for i in range(4)]):
                    num_lines += 1
        return num_lines

    def move(self, column):
        new_state = State()
        
        # Copy the board
        new_state.board = [row[:] for row in self.board]

        # Copy other fields
        new_state.column_heights = self.column_heights[:]
        new_state.available_moves = self.available_moves[:]
        new_state.player = 3 - self.player

        # Apply the move
        row = new_state.column_heights[column]
        new_state.board[row][column] = self.player
        if row == 0:
            new_state.available_moves.remove(column)
        else:
            new_state.column_heights[column] -= 1

        new_state.update_winner()
        return new_state

    def update_winner(self):
        if self.count_lines(4, 1) > 0:
            self.winner = 1
        elif self.count_lines(4, 2) > 0:
            self.winner = 2
        elif not self.available_moves:
            self.winner = 0

def column_features(state: State, col: int):
    s2 = deepcopy(state).move(col)
    f0 = 1 if s2.winner == state.player else 0
    f1 = 0
    if f0 == 0:
        for c2 in s2.available_moves:
            if s2.move(c2).winner == (3 - state.player):
                f1 = 1
                break
    f2 = 1 if state.count_lines(3, state.player) < s2.count_lines(3, state.player) else 0
    f3 = 0
    for c2 in state.available_moves:
        if deepcopy(state).move(c2).winner == (3 - state.player):
            f3 = 1
            break
    f4 = 1 if col == NUM_COLS // 2 else 0
    return [f0, f1, f2, f3, f4]

def build_feature_dataset(match_data):
    rows = []
    for idx, rec in match_data.iterrows():
        state = State()
        flat = [rec[f'cell_{i}'] for i in range(42)]
        for i, val in enumerate(flat):
            r, c = divmod(i, NUM_COLS)
            state.board[r][c] = val
        state.player = rec['player']
        feats = []
        for col in state.available_moves:
            feats += column_features(state, col)
        label = state.available_moves.index(rec['mtcarlomove'])
        rows.append((feats, label))

    X, y = [], []
    for rec in rows:
        feat_vec, lbl = rec
        if len(feat_vec) < 5*NUM_COLS:
            feat_vec += [0] * (5*NUM_COLS - len(feat_vec))
        X.append(feat_vec)
        y.append(lbl)

    return pd.DataFrame(X, columns=[f'f{i}' for i in range(5*NUM_COLS)]), pd.Series(y)

def train_single_tree(args):
    X, y, max_depth = args
    tree = ID3DecisionTree()
    N = len(X)
    idx = np.random.choice(N, N, replace=True)
    tree.fit(X.iloc[idx], y.iloc[idx], max_depth=max_depth)
    return tree

def train_ensemble(match_data, n_trees: int = 7, max_depth: int = 7, save_path=None):
    X, y = build_feature_dataset(match_data)
    args_list = [(X, y, max_depth)] * n_trees

    start = time.time()
    with ProcessPoolExecutor() as executor:
        ensemble = list(executor.map(train_single_tree, args_list))
    total_time = time.time() - start

    if save_path:
        joblib.dump(ensemble, save_path, compress=3)

    return ensemble, round(total_time, 2)

def trainnn(p, difficulty="Medium"):
    try:
        if os.path.exists("match_log.parquet"):
            md = pd.read_parquet("match_log.parquet")
            hash_now = compute_file_hash("match_log.parquet")
        elif os.path.exists("match_log.csv"):
            md = pd.read_csv("match_log.csv", on_bad_lines='skip')
            hash_now = compute_file_hash("match_log.csv")
        else:
            print("🔸 No match_log file found; skipping training.")
            return

        hash_file1 = f"trees_p1_{difficulty.lower()}.hash"
        hash_file2 = f"trees_p2_{difficulty.lower()}.hash"

        md = md[md['mtcarlomove'].notnull()]
        md['board_sum'] = md[[f'cell_{i}' for i in range(42)]].sum(axis=1)
        md = md[md['board_sum'] > 10]
        md['board_hash'] = md.apply(hash_board, axis=1)
        md.drop_duplicates(subset=['board_hash', 'player'], inplace=True)

        data1 = md[md['player'] == 1]
        data2 = md[md['player'] == 2]
        estimated_time = 0
        config = ID3_DIFFICULTY_CONFIG.get(difficulty, ID3_DIFFICULTY_CONFIG["Medium"])

        path1 = f"trees_p1_{difficulty.lower()}.pkl"
        path2 = f"trees_p2_{difficulty.lower()}.pkl"

        global learned_trees_p1, learned_trees_p2

        if data1.empty or (os.path.exists(hash_file1) and open(hash_file1).read().strip() == hash_now):
            print("🔸 Skipping Player 1 training — no new data.")
        else:
            learned_trees_p1, est1 = train_ensemble(data1, **config, save_path=path1)
            estimated_time += est1
            with open(hash_file1, 'w') as f:
                f.write(hash_now)

        if data2.empty or (os.path.exists(hash_file2) and open(hash_file2).read().strip() == hash_now):
            print("🔸 Skipping Player 2 training — no new data.")
        else:
            learned_trees_p2, est2 = train_ensemble(data2, **config, save_path=path2)
            estimated_time += est2
            with open(hash_file2, 'w') as f:
                f.write(hash_now)

        return {1: learned_trees_p1, 2: learned_trees_p2}, estimated_time

    except FileNotFoundError:
        print("🔸 match_log file not found; skipping training.")

def load_saved_trees(difficulty="Medium"):
    global learned_trees_p1, learned_trees_p2
    try:
        path1 = f"trees_p1_{difficulty.lower()}.pkl"
        path2 = f"trees_p2_{difficulty.lower()}.pkl"
        if os.path.exists(path1):
            learned_trees_p1 = joblib.load(path1)
        if os.path.exists(path2):
            learned_trees_p2 = joblib.load(path2)
        return {1: learned_trees_p1, 2: learned_trees_p2}
    except Exception as e:
        print(f"⚠️ Could not load saved trees: {e}")

def execute_learned_move(tree):
    def inner(game):
        st = game.state
        feat = []
        for col in range(NUM_COLS):
            if col in st.available_moves:
                feat += column_features(st, col)
            else:
                feat += [0]*5
        row = pd.Series(feat, index=[f'f{i}' for i in range(5 * NUM_COLS)])
        try:
            pred = tree.predict_one(row)
            if pred is None:
                raise ValueError("Previsão da árvore foi None.")
            if 0 <= pred < len(st.available_moves):
                return st.available_moves[pred]
            else:
                raise ValueError(f"Previsão inválida: {pred} para available_moves: {st.available_moves}")
        except Exception as e:
            print(f"⚠️ Fallback para jogada aleatória (erro na IA): {e}")
            return random.choice(st.available_moves)
    return inner

def make_ensemble_ai(trees_list):
    def inner(game):
        st = game.state
        feat = []
        for col in range(NUM_COLS):
            if col in st.available_moves:
                feat += column_features(st, col)
            else:
                feat += [0]*5
        row = pd.Series(feat, index=[f'f{i}' for i in range(5 * NUM_COLS)])
        votes = [t.predict_one(row) for t in trees_list]
        try:
            best = Counter(votes).most_common(1)[0][0]
            if 0 <= best < len(st.available_moves):
                return st.available_moves[best]
            else:
                raise ValueError(f"Voted move index {best} is invalid for available moves {st.available_moves}")
        except Exception as e:
            print(f"⚠️ Ensemble fallback due to error: {e}")
            return random.choice(st.available_moves)
    return inner

