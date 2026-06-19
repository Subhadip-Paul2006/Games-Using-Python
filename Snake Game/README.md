# 🐍 Snake Game (Python)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyGame-005F0F?style=for-the-badge&logo=python&logoColor=white" alt="PyGame"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge" alt="Status"/>
</p>

A classic **Snake Game** built using **Python and Pygame**, complete with a **PostgreSQL** leaderboard, gradient-shaded snake rendering, normal food, and randomly spawning **bonus food**.

---

## 📌 Project Status

✅ **Complete** — playable end-to-end with persistent high-score storage.

---

## 🎮 Game Description

The player controls a snake that moves around a gridded board.  
The goal is to eat food, grow longer, and avoid colliding with the walls or itself.  
A higher score is rewarded by snagging rare pulsing **gold bonus food** (+50 points).

---

## ✨ Features

- 🐍 Smooth snake movement with **gradient body coloring** (head cyan → tail purple)
- 🍎 Random food generation that never overlaps the snake
- ⭐ Pulsing **gold bonus food** (+50 points, appears every 7–10 s)
- 📈 Real-time score tracking + persistent high-score DB
- 🎨 Polished start screen with player-name input
- 🛑 Wall + self-collision detection
- 💥 Game-over screen with **NEW HIGH SCORE!** celebration

---

## 🕹️ Game Loop

```mermaid
flowchart TD
    Start([Start python snake_game.py]) --> DB[Connect PostgreSQL]
    DB --> Init[Initialize PyGame + Grid]
    Init --> StartScreen[Show Start Screen + Name Input]
    StartScreen -- "ENTER" --> Spawn[Spawn Snake + Food]
    Spawn --> Loop{Tick 10 FPS}
    Loop --> Input[Read Keyboard Events]
    Input --> Move[Compute Next Head Position]
    Move --> Wall{Hits Wall?}
    Wall -- Yes --> GameOver[Game Over Screen]
    Wall -- No --> Self{Hits Self?}
    Self -- Yes --> GameOver
    Self -- No --> EatFood{Head == Food?}
    EatFood -- "Normal" --> Grow[+10 Pts, Respawn Food]
    EatFood -- "Bonus" --> BonusGrow[+50 Pts, Remove Bonus]
    EatFood -- "No" --> Slide[Pop Tail, Slide Forward]
    Grow --> Render
    BonusGrow --> Render
    Slide --> Render
    Render --> BonusTime{Bonus Timer?}
    BonusTime -- "Spawn" --> Render
    BonusTime -- "Continue" --> Loop
    GameOver --> Save[Save Score to DB]
    Save --> Wait[Wait 5 s + Exit]
```

---

## 🐍 Snake Lifecycle

```mermaid
sequenceDiagram
    participant Player
    participant Snake
    participant Board
    participant DB

    Player->>Snake: W / A / S / D key
    Snake->>Snake: next_direction = (dx, dy)
    Snake->>Board: new_head = head + direction
    alt Collision
        Board-->>Snake: Game Over
        Snake->>DB: save_score_to_db(name, score, high)
    else Eats Food
        Board-->>Snake: score += 10, grow tail
    else Eats Bonus
        Board-->>Snake: score += 50
    else Empty Move
        Board-->>Snake: pop tail (no growth)
    end
    Snake->>Board: render gradient cells
```

---

## 🎨 Board Visualization

```text
┌──────────────────────────────────────────────────────┐
│  Score: 10                High Score: 240            │
│                                                      │
│   ┌──┐                                                │
│   │  │                                                │
│   │  │   🐍🐍🐍                                       │
│   │  │       🐍        ⭐ (gold bonus, pulsing)       │
│   │  │       🐍🐍                                     │
│   └──┘                                                │
│                                                      │
└──────────────────────────────────────────────────────┘
   Grid: 40 × 30 cells of 20×20 px   →   800 × 600 px
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| 🐍 Language | Python 3.x |
| 🎮 Engine | PyGame |
| 💾 Database | PostgreSQL (psycopg2) |
| 📦 Distribution | Standalone `.py` script |

---

## 📂 Project Structure

```text
Snake Game/
│
├── snake_game.py     # 🎮 Full game logic, rendering, DB
├── requirements.txt  # 📦 Pinned dependencies
└── README.md         # 📖 You are here
```

---

## ⚙️ Game Constants

```mermaid
classDiagram
    class Window {
        +int WINDOW_WIDTH = 800
        +int WINDOW_HEIGHT = 600
        +int GRID_SIZE = 20
        +int FPS = 10
    }

    class Snake {
        +list snake_body
        +list direction
        +list next_direction
        +GradientColor head_to_tail()
    }

    class Food {
        +list normal_food
        +list bonus_food
        +int bonus_spawn_interval = 7-10s
        +int bonus_duration = 2.5-3.5s
    }

    class Database {
        +str host = localhost
        +int port = 5432
        +str database = snake_game_db
        +fetch_high_score()
        +save_score_to_db()
    }

    Window --> Snake
    Snake --> Food
    Database --> Snake
```

---

## 🗄️ Database Schema

```mermaid
erDiagram
    SNAKE_GAME_SCORES {
        int       id PK
        varchar   player_name
        int       score
        boolean   is_high_score
        timestamp played_at
    }
```

---

## 🎯 Controls

| Action | Key |
|--------|-----|
| ⬆️ Move Up | <kbd>W</kbd> |
| ⬇️ Move Down | <kbd>S</kbd> |
| ⬅️ Move Left | <kbd>A</kbd> |
| ➡️ Move Right | <kbd>D</kbd> |
| ▶️ Start Game | <kbd>Enter</kbd> |
| ⌫ Delete Character | <kbd>Backspace</kbd> |

> The snake cannot directly reverse direction onto itself — input is buffered until the next tick.

---

## 📊 Scoring Rules

```mermaid
pie title Points Per Pickup
    "Normal Food (+10)" : 10
    "Bonus Food (+50)" : 50
```

| Event | Points |
|-------|:------:|
| 🍎 Eat normal food | **+10** |
| ⭐ Eat bonus food | **+50** |
| 💥 Wall collision | Game Over |
| 💥 Self collision | Game Over |

---

## ▶️ How to Run the Game

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure PostgreSQL

Update the `DB_CONFIG` dictionary in `snake_game.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'snake_game_db',
    'user': 'postgres',
    'password': 'subh06'
}
```

### 3️⃣ Create the table

```sql
CREATE TABLE snake_game_scores (
    id            SERIAL PRIMARY KEY,
    player_name   VARCHAR(50)  NOT NULL,
    score         INT          NOT NULL,
    is_high_score BOOLEAN      DEFAULT FALSE,
    played_at     TIMESTAMP    DEFAULT NOW()
);
```

### 4️⃣ Launch

```bash
python snake_game.py
```

---

## 🧠 Game Architecture

```mermaid
flowchart LR
    A[Game Init] --> B[fetch_high_score]
    B --> C[show_start_screen]
    C --> D[run_game loop]
    D --> E{Input Event}
    E -->|WASD| F[Update direction]
    F --> G[Compute new head]
    G --> H{Collision}
    H -- Yes --> I[show_game_over_screen]
    H -- No --> J{Eats Food?}
    J -- Normal --> K[+10 Pts, Respawn]
    J -- Bonus --> L[+50 Pts]
    J -- None --> M[Slide Tail]
    K --> N[Render Frame]
    L --> N
    M --> N
    N --> D
    I --> O[save_score_to_db]
    O --> P([Exit])
```

---

## 🚀 Future Improvements

- 🔊 Sound effects (eat / crash / bonus)
- 💾 High-score saving (already implemented — extend to top-10 leaderboard)
- ⏸ Pause / Resume feature
- 🎚 Difficulty levels (speed scaling)
- 🌐 Web export via Pyodide / Pygbag

---

## 👨‍💻 Author

- **Subh** & **Abhishek**

---

<p align="center">
  🐍 A retro classic reimagined with a modern twist.
</p>
