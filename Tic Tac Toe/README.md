# 🎮 Tic Tac Toe — Single Player (Python + PyGame)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyGame-005F0F?style=for-the-badge&logo=python&logoColor=white" alt="PyGame"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge" alt="Status"/>
</p>

A **Single Player Tic Tac Toe game** built using **Python and PyGame**, with **database integration** for storing game-related data.

---

## 📌 Basic Information

| Property | Value |
|----------|-------|
| 🎲 **Game Name** | Tic Tac Toe |
| 👤 **Mode** | Single Player (vs Computer AI) |
| 🐍 **Language** | Python |
| 🎮 **Framework** | PyGame |
| 💾 **Database** | SQLite / PostgreSQL (configurable via `.env`) |

---

## 🎯 Game Objective

The objective is to align **three identical symbols** before the opponent does:

- ↔️ **Horizontally**
- ↕️ **Vertically**
- ↗️ **Diagonally**

---

## 🏁 The 3×3 Grid — Coordinates

```text
      col 0     col 1     col 2
     ┌─────────┬─────────┬─────────┐
row  │ (0,0)   │ (1,0)   │ (2,0)   │
  0  │   ⭕    │         │   ❌    │
     ├─────────┼─────────┼─────────┤
row  │ (0,1)   │ (1,1)   │ (2,1)   │
  1  │   ❌    │   ⭕    │         │
     ├─────────┼─────────┼─────────┤
row  │ (0,2)   │ (1,2)   │ (2,2)   │
  2  │         │   ❌    │   ⭕    │
     └─────────┴─────────┴─────────┘
```

---

## 🏆 The 8 Winning Patterns

```mermaid
flowchart LR
    subgraph Rows["↔️ Horizontal Wins"]
      R0[Row 0: r0c0-r0c1-r0c2]
      R1[Row 1: r1c0-r1c1-r1c2]
      R2[Row 2: r2c0-r2c1-r2c2]
    end
    subgraph Cols["↕️ Vertical Wins"]
      C0[Col 0: r0c0-r1c0-r2c0]
      C1[Col 1: r0c1-r1c1-r2c1]
      C2[Col 2: r0c2-r1c2-r2c2]
    end
    subgraph Diag["↗️ Diagonal Wins"]
      D1[Desc: r0c0-r1c1-r2c2]
      D2[Asc:  r2c0-r1c1-r0c2]
    end
```

```text
   0   1   2
0  ●───●───●     ← Row 0 win
   │ ╲ │ ╱ │
1  ●───●───●     ← Row 1 win
   │ ╱ │ ╲ │
2  ●───●───●     ← Row 2 win
   ↑   ↑   ↑
   Col  Col  Col
   0    1    2
        ╲ ╱
         ●        ← Diagonals
```

---

## 🔄 Game Flow

```mermaid
flowchart TD
    A([🚀 Launch main.py]) --> B[Show Player Name Input Screen]
    B --> C[Player 1 Name] --> D[Player 2 Name]
    D --> E[Initialize Board: 3×3 grid]
    E --> F[Draw Lines + Empty Board]

    F --> G{current_player?}
    G -- "Player 1 ⭕" --> H[Wait for Mouse Click]
    H --> I{Empty Square?}
    I -- "No" --> H
    I -- "Yes" --> J[Mark Square with ⭕]
    J --> K{check_win?}
    K -- "Yes" --> L[Draw Winning Line]
    L --> M[Show Winner Screen]
    K -- "No"  --> N{Board Full?}
    N -- "Yes" --> O[🤝 Draw Screen]
    N -- "No"  --> P[Switch to Player 2 ❌]

    G -- "Player 2 ❌" --> H2[Wait for Mouse Click]
    H2 --> I
    J2[Mark Square with ❌] --> K

    M --> Q{Save to DB?}
    Q -- "Yes" --> R[(Update DBManager)]
    Q -- "No"  --> S[Restart]
    O --> S
    R --> S[Restart or Quit]
```

---

## 🧠 Win Detection Logic

```mermaid
flowchart TB
    A[check_win player] --> B[Loop over Columns]
    B --> C{board 0,c,1,c,2,c all == player?}
    C -- "Yes" --> Z[✅ Vertical Win]
    C -- "No"  --> D[Loop over Rows]
    D --> E{board r,0,r,1,r,2 all == player?}
    E -- "Yes" --> Z2[✅ Horizontal Win]
    E -- "No"  --> F{Diagonal Descending?}
    F -- "Yes" --> Z3[✅ Diagonal Win]
    F -- "No"  --> G{Diagonal Ascending?}
    G -- "Yes" --> Z4[✅ Diagonal Win]
    G -- "No"  --> H[❌ No Win]
```

---

## 🖱 Input → Cell Mapping

```text
Mouse (x, y)
       │
       ▼
   row = y // 200
   col = x // 200
       │
       ▼
  board[row][col] = current_player
```

```mermaid
sequenceDiagram
    participant User
    participant Pygame
    participant Logic

    User->>Pygame: Click at (x, y)
    Pygame->>Logic: row=y//200, col=x//200
    Logic->>Logic: available_square?
    alt Empty
        Logic->>Logic: mark_square(row, col, player)
        Logic->>Logic: check_win(player)
    else Occupied
        Logic-->>User: ignore click
    end
```

---

## 🎨 Visual Layers

```mermaid
flowchart LR
    A[Background Fill BG_COLOR] --> B[Draw Grid Lines]
    B --> C[Loop over Board Cells]
    C --> D{cell value?}
    D -- "1" --> E[Draw ⭕ Circle]
    D -- "2" --> F[Draw ❌ Cross]
    D -- "0" --> G[Skip Empty]
    E --> H[Draw Score / Status]
    F --> H
    G --> H
```

---

## 🏗️ Module Architecture

```mermaid
flowchart TB
    subgraph Presentation["🎨 Presentation Layer"]
        DrawLines[draw_lines - Grid]
        DrawFigures[draw_figures - X/O]
        DrawWinLine[Winning Line Renderer]
    end

    subgraph Logic["⚙️ Game Logic"]
        MarkSquare[mark_square]
        Available[available_square]
        CheckWin[check_win]
        Restart[restart_game]
        InputScreen[input_screen - Names]
    end

    subgraph Data["💾 Data Layer"]
        DBManager[DBManager]
        EnvCfg[.env config]
    end

    Presentation --> Logic
    Logic --> Data
```

---

## 📂 Project Structure

```text
Tic Tac Toe/
│
├── main.py         # 🎮 Game loop, board, rendering, win detection
├── db_manager.py   # 💾 DBManager wrapper for stats persistence
├── db_utils.py     # 🔌 Helpers for query construction
├── .env            # 🔐 Environment variables (DB credentials)
├── requirements.txt# 📦 Pinned dependencies
└── README.md       # 📖 You are here
```

---

## 🗄️ Database Schema

```mermaid
erDiagram
    GAMES {
        int      id PK
        varchar  player1_name
        varchar  player2_name
        varchar  winner
        int      total_moves
        timestamp played_at
    }
```

---

## 🎮 Playing Rules

1. 🎲 The game is played on a **3×3 grid**.
2. 🖱 The player clicks on an empty cell to make a move.
3. 🚫 Each cell can be used only once.
4. 🏆 A win is declared if **three symbols align**.
5. 🤝 If all cells are filled and no win is formed → **draw**.
6. 🔁 The game can be **restarted** after completion.

---

## 🛠 Requirements

- 🐍 Python 3.x
- 🎮 PyGame
- 📦 Libraries listed in `requirements.txt`

---

## ▶️ How to Run the Game

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure environment

Create a `.env` file with your DB credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tic_tac_toe_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3️⃣ Launch the game

```bash
python main.py
```

---

## 🗺️ Game Tree — Player 1 Perspective

```mermaid
flowchart TB
    Start((Start)) --> A1[Player 1 Move]
    A1 --> A2[Center?]
    A2 -- "Yes" --> B1[Strong Position]
    A2 -- "No"  --> B2[Corner?]
    B2 -- "Yes" --> B3[Decent Position]
    B2 -- "No"  --> B4[Weak - Edge]

    B1 --> C1{Opponent Blocks Center?}
    C1 -- "Yes" --> C2[Try Corners]
    C1 -- "No"  --> C3[Build Lines]

    B3 --> D1{Make Fork?}
    D1 -- "Yes" --> D2[2-Way Threat]
    D1 -- "No"  --> D3[Defensive Play]
```

---

## 🎨 Color Palette

| Token | Color | Hex |
|-------|-------|-----|
| Background | 🟦 Teal | `#1CAA9C` |
| Grid Lines | 🟢 Dark Teal | `#179187` |
| ⭕ Circle | 🟡 Cream | `#EFE7C8` |
| ❌ Cross | ⬛ Dark Grey | `#424242` |
| Win Line | 🟢 Green / 🔴 Red | Dynamic |

---

## 🚀 Future Improvements

- 🌐 Multiplayer over network
- 🤖 Smarter AI (Minimax algorithm)
- 📈 ELO rating system
- 🎞 Animations for X / O placement
- 📱 Mobile / Web export (Pygbag)

---

## 📜 License

This project is part of the **Games-Using-Python** collection under the **MIT License**.

---

<p align="center">
  ⭕ ❌ Three in a row wins it all.
</p>
