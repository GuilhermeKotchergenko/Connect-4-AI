# Connect‑4‑AI

> **Play, train & compare AI agents for the classic Connect Four** — ID3 decision trees, ensemble bagging, and (parallel) Monte‑Carlo Tree Search implemented in pure Python and orchestrated from a single Jupyter notebook.

---

## ✨ Features at a glance

| Category                  | Highlights                                                                                                                                                                                                             |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Game engine**           | 6 × 7 Connect Four with full rule enforcement & win detection (Python) + terminal UI                                                                                                                                   |
| **Game modes**            | • Player vs Player  • Player vs Computer  • Computer vs Computer                                                                                                                                                       |
| **AI agents**             | ① *Random* baseline <br>② *ID3 Decision Tree* trained from self‑play logs <br>③ *Decision‑Tree Ensemble* (bootstrap + majority vote) <br>④ *Monte‑Carlo Tree Search* (UCT) <br>⑤ *Parallel MCTS* via `multiprocessing` |
| **Learning loop**         | Every finished match is appended to `datasets/match_log.csv`; choosing a tree‑based agent triggers automatic re‑training                                                                                               |
| **Visualisation**         | Graphviz exports for decision trees & MCTS trees, plus matplotlib win‑rate plots                                                                                                                                       |
| **Reproducible notebook** | `connect_four.ipynb` runs all experiments and produces the figures you see in `images/`                                                                                                                                |

---

## 🚀 Quick start

### 1  Install requirements

```bash
# clone the repo
git clone https://github.com/<your‑user>/Connect‑4‑AI.git
cd Connect‑4‑AI

# optional: create a virtual‑env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install Python packages
pip install -r requirements.txt
```

> **Graphviz** must be available **system‑wide** for the export helpers to work — e.g. `sudo apt install graphviz` (Linux) or install from [https://graphviz.org/download](https://graphviz.org/download) and add `bin/` to `%PATH%` (Windows).

### 2  Run from the terminal

The runnable script lives inside the sub‑folder **`Nanahira Connect 4!/main.py`**:

```bash
python "Nanahira Connect 4!/main.py"
```

Follow the interactive menu to pick a game mode and choose an AI for each player.

### 3  Reproduce the notebook experiments

Open **`connect_four.ipynb`** in Jupyter Lab/Notebook and execute the cells.  The notebook will:

* launch configurable match‑ups (e.g. *Random vs MCTS*, *DT vs Ensemble*),
* log every move to `datasets/`,
* create diagrams under `images/` and model snapshots (`*.pkl`, `*.hash`) under **`Nanahira Connect 4!/`**.

---

## 📁 Repository layout

```text
Connect‑4‑AI/
├── datasets/                 # CSV logs & benchmark datasets
│   ├── baddata.csv
│   ├── big.csv
│   ├── imbalanced.csv
│   ├── match_log.csv         # grows after every game
│   ├── mixed.csv
│   └── performance_log.csv
├── images/                   # Graphviz & matplotlib outputs
│   ├── mcts_root.png
│   ├── mcts_tree.png
│   ├── minha_arvore.dot
│   └── minha_arvore.png
├── Nanahira Connect 4!/      # main application package
│   ├── Assets/               # (if using Unity – otherwise ignore)
│   ├── Nanahira/             # src package
│   ├── main.py               # ← entry point used by the README
│   ├── main.spec             # PyInstaller spec (for binary builds)
│   ├── match_log.csv         # separate log for this build
│   ├── trees_p*_*.pkl        # pickled decision‑tree models
│   └── trees_p*_*.hash       # saved model hashes
├── References/               # playground & example notebooks
│   ├── iris_decision_tree.ipynb
│   └── iris.csv
├── connect_four.ipynb        # master notebook (same code as main.py but with experiments)
├── requirements.txt
└── README.md                 # you are here
```

*(Folder names with spaces are quoted in shell commands above for safety.)*

---

## 🧠 Inside the code

1. **State representation** — `State` tracks the 6 × 7 board, legal moves, current player and winner status.
2. **Feature engineering** — each candidate column is described by five boolean/int features:

   * immediate win (`f0`)
   * blocks opponent win (`f1`)
   * forms exactly one 3‑in‑a‑row (`f2`)
   * prevents opponent threat (`f3`)
   * centre‑column bonus (`f4`)
3. **ID3 Decision Tree** — implemented from scratch with entropy & information‑gain splitting; predicts the *index inside* `available_moves`.
4. **Bagging Ensemble** — `train_ensemble` bootstraps *N* trees and `make_ensemble_ai` applies majority vote.
5. **Monte‑Carlo Tree Search** — UCT selection, back‑prop with configurable reward (win=1, draw=0 or 0.5) and optional parallel roll‑outs.
6. **Self‑play logging** — every completed game is flattened and appended to CSV; models are retrained on next invocation.

---

## 📊 Example benchmark results

| Match‑up (100 games)                    | Win % P1 | Win % P2 | Draw % |
| --------------------------------------- | -------: | -------: | -----: |
| Random vs Random                        |     51.0 |     49.0 |    0.0 |
| Random vs MCTS (100 epochs)             |     4.0 |     96.0 |    0.0 |
| Random vs Parallel-MCTS (100 epochs)    |     6.0 |     94.0 |    0.0 |
| Parallel‑MCTS (100) vs Itself           |     56.0 |     44.0 |    0.0 |
| Parallel‑MCTS (100) vs Itself (Reward Draw=0.5)          |     63.0 |     37.0 |    0.0 |
| Parallel‑MCTS (100) vs Itself (C=1)          |     62.0 |     38.0 |    0.0 |
| Parallel‑MCTS (100) vs Itself (C=2)          |     70.0 |     30.0 |    0.0 |
| Parallel‑MCTS (100) vs Itself (MaxChildrenExpandedNodes=4)          |     70.0 |     30.0 |    0.0 |
| Parallel‑MCTS (100) vs (1000 epochs)    |     19.0 |     81.0 |    0.0 |
| Decision Tree (Bad dataset by random simulation) vs Random  |     53.0 |     47.0 |    0.0 |
| Decision Tree (Mixed dataset mostly by MC) vs Random  |     86.0 |     14.0 |    0.0 |
| Decision Tree (Big dataset only by MC) vs MC  |     26.0 |     74.0 |    0.0 |
| Decision Tree (Mixed) vs Ensemble Vote (Mixed)  |     24.0 |     76.0 |    0.0 |

*(Your numbers will vary — run the notebook to reproduce.)*

---

## 🛠️ Train on your own games

```python
import pandas as pd
from Nanahira.train import train_ensemble, build_feature_dataset  # adjust to your package structure

my_matches = pd.read_csv("datasets/my_match_log.csv")
ensemble = train_ensemble(my_matches, n_trees=7, max_depth=6)
```

---

## 🤝 Contributing

1. Fork & clone your fork.
2. Create a feature branch `git checkout -b feat/my‑feature`.
3. Run `ruff`/`flake8`, commit, push, and open a PR.

---

## 📄 License

Released under the **MIT License** — see `LICENSE`.

---

*Have fun exploring game AI!*
