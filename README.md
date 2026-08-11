# 🎮 Games Using Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyGame-005F0F?style=for-the-badge&logo=python&logoColor=white" alt="PyGame"/>
  <img src="https://img.shields.io/badge/Tkinter-FF8C00?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT"/>
</p>

<p align="center">
  <strong>A collection of classic games built with Python — designed to grow into a unified Web &amp; Android gaming platform.</strong>
</p>

---

## 🌟 Project Vision at a Glance

```text
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│   Individual Python Games  ──►  Modular Core  ──►  Platform    │
│   (Snake, Flappy, Tetris,       (shared UI,       (Web App +   │
│    RPS, Hangman, Mines,          leaderboard,     Android App) │
│    Tic-Tac-Toe, Pong)            login, theme)                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

The long-term goal of this repository is to build a **single platform (Web App / Android App)** that hosts multiple classic games developed using Python.

These games are currently being built and tested individually.  
In the future, they will be integrated into a **centralized gaming application** where users can:

- 🌐 Browse and play multiple classic games
- 🪟 Access games from a single interface
- 🎯 Experience smooth and interactive gameplay
- 💡 Enjoy a lightweight casual gaming platform

This repository serves as the **development and experimentation ground** for those games before they are integrated into the final application.

---

## 🗺️ Roadmap Timeline

```mermaid
gantt
    title Games-Using-Python — Development Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b %Y

    section Phase 1 — Core Games
    Tic Tac Toe          :done,    ttt, 2025-01-15, 30d
    Snake Game           :done,    snk, 2025-01-20, 25d
    Hangman              :done,    hng, 2025-02-10, 20d
    Rock Paper Scissors  :done,    rps, 2025-03-01, 25d
    MineSneeker          :done,    min, 2025-03-05, 30d
    Flappy Bird          :done,    fly, 2025-03-08, 18d
    Tetris               :done,    tet, 2025-03-12, 20d

    section Phase 2 — Polish
    UI/UX improvements         :active,  ui,  2026-04-01, 90d
    Modular package structure  :         mod, 2026-05-01, 60d
    Shared leaderboard service :         lb,  2026-06-01, 60d

    section Phase 3 — Platform
    Web Application (Flask)    :         web, 2026-08-01, 120d
    Android App (Kivy/Buildozer):       and, 2026-10-01, 150d
```

### Roadmap Checklist

- ✅ Develop individual games using Python
- 🚧 Improve UI and gameplay experience
- 📦 Organize games into a modular structure
- 🌐 Build a **Web Application** to host all games
- 📱 Develop an **Android App** version of the platform

---

## 📊 Game Status Overview

> ⚠️ Please read the `README.md` inside each project folder before running the game.

| # | Game | Status | Developed By | Engine | Database |
|---|------|:------:|--------------|--------|:--------:|
| 1 | 🟦 Tic Tac Toe | ✅ Completed | Subh & Abhishek | PyGame | ✅ |
| 2 | 🐍 Snake Game | ✅ Completed | Subh & Abhishek | PyGame | ✅ |
| 3 | 🐦 Flappy Bird | ✅ Completed | Abhishek & Samhita | PyGame | ✅ |
| 4 | 🏓 Pong Game | 📌 Planned | Subh & Abhishek | PyGame | ❌ |
| 5 | 🔤 Hangman | ✅ Completed | Subh | PyGame | ❌ |
| 6 | 💣 MineSneeker | ✅ Completed | Subh | Tkinter | ✅ |
| 7 | ✊ Rock Paper Scissors | ✅ Completed | Subh | Tkinter | ✅ |
| 8 | 🧱 Tetris | ✅ Completed | Subh | PyGame | ❌ |

### Completion Donut

```mermaid
pie title Repository Completion
    "Completed Games" : 7
    "Planned Games"   : 1
```

---

## 🎮 Games Included

```mermaid
mindmap
  root((Games Using Python))
    Arcade
      Flappy Bird
      Tetris
    Puzzle
      MineSneeker
      Tic Tac Toe
    Word & Chance
      Hangman
      Rock Paper Scissors
    Classic
      Snake Game
      Pong (upcoming)
```

### 🐍 Snake Game
Move the snake & beat the highest score. Bonus food appears randomly with a pulsing gold glow.

### 🐦 Flappy Bird
Navigate the bird through pipes without crashing. Coins drop between pipes for extra points.

### 🔤 Hangman
Guess the hidden word before the hangman drawing completes. Modern dark-themed UI with on-screen keyboard.

### ❌ Tic Tac Toe
Just play it with your partner, friend, parents and enjoy... Single-player PyGame version with database.

### 💣 MineSneeker
Guess the mine, and your game is over. Multiple difficulty modes and persistent leaderboard.

### ✊ Rock Paper Scissors
Experience playing rock paper scissors virtually on PC. Includes login, series gameplay and global leaderboard.

### 🧱 Tetris
A polished PyGame Tetris with procedural sound, neon palettes and 3D beveled block rendering.

### 🏓 Pong (Upcoming)
Two-player paddle game inspired by the classic arcade.

---

## 🧱 Repository Architecture

```text
Games-Using-Python/
│
├── 📁 Flappy Bird/            # 🐦 Pure PyGame arcade with coin pickups
│   ├── Flappy_Bird.py
│   ├── assests/
│   │   ├── images/            # Bird and coin sprites
│   │   └── sounds/            # Flap, point, hit, die, swoosh SFX
│   ├── .env
│   ├── requirements.txt
│   └── README.md
│
├── 📁 Hangman/                # 🔤 Modern dark-themed PyGame hangman
│   ├── main.py
│   ├── words.txt
│   ├── generate_sounds.py
│   ├── hangman0..6.png
│   ├── *.wav
│   └── README.md
│
├── 📁 MineSneeker/            # 💣 Tkinter minesweeper + Postgres
│   ├── main.py
│   ├── db_manager.py
│   ├── assets/
│   │   └── sounds/            # Game audio effects
│   └── README.md
│
├── 📁 Rock Paper Scissors/    # ✊ Tkinter RPS w/ login + leaderboard
│   ├── main.py
│   ├── loginGame.py
│   ├── db_manager.py
│   ├── setup_db.py
│   ├── Images/                # Sprites and screenshots
│   └── README.md
│
├── 📁 Snake Game/             # 🐍 PyGame snake with PostgreSQL leaderboard
│   ├── snake_game.py
│   ├── requirements.txt
│   └── README.md
│
├── 📁 Tetris Game/            # 🧱 PyGame Tetris w/ procedural audio
│   ├── tetris.py
│   ├── block.py
│   ├── constants.py
│   ├── generate_sounds.py
│   ├── *.wav                  # Procedural 8-bit audio
│   └── README.md
│
├── 📁 Tic Tac Toe/            # ❌ PyGame tic-tac-toe w/ Postgres
│   ├── main.py
│   ├── db_manager.py
│   ├── db_utils.py
│   ├── requirements.txt
│   └── README.md
│
├── 📄 APP_DEVELOPMENT.md      # 📱 Flutter & Firebase App Roadmap
├── 📄 DESIGN.md               # 🎨 Design System & UI Specs
├── 📄 PRD.md                  # 📋 Product Requirements Document
├── 📄 TRD.md                  # 🛠 Technical Requirements Document
├── 📄 README.md               # ⬅️ Root documentation
└── 📄 .gitignore
```

---

## 🧠 Shared Architecture Across Games

```mermaid
flowchart LR
    subgraph Client["🎮 Game Client (PyGame / Tkinter)"]
        UI[UI Layer]
        LOGIC[Game Logic]
        INPUT[Input Handler]
    end

    subgraph Core["⚙️ Shared Services (Future)"]
        AUTH[Auth Service]
        LB[Leaderboard Service]
        THEME[Theme Engine]
    end

    subgraph Data["💾 Data Layer"]
        PG[(PostgreSQL)]
        JSON[(JSON Fallback)]
    end

    UI <--> LOGIC
    LOGIC <--> INPUT
    LOGIC -.-> AUTH
    LOGIC -.-> LB
    UI -.-> THEME

    AUTH --> PG
    LB  --> PG
    LB  -.-> JSON
```

---

## 🛠️ Tech Stack Distribution

```mermaid
pie title Lines of Code per Game (approx.)
    "Snake Game"           : 350
    "Flappy Bird"          : 215
    "Hangman"              : 350
    "MineSneeker"         : 1100
    "Rock Paper Scissors"  : 700
    "Tetris"               : 420
    "Tic Tac Toe"          : 320
```

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.x |
| **Game Engine** | PyGame 2.x |
| **GUI Toolkit** | Tkinter (RPS, MineSneeker) |
| **Database** | PostgreSQL (psycopg2) |
| **Image Rendering** | Pillow (PIL) |
| **Audio** | PyGame Mixer / Wave (procedural) |

---

## 🚀 Goal of This Repository

This repository is a personal project to explore **game development using Python** by recreating classic games. Each game demonstrates different concepts of programming, UI rendering, and interactive gameplay. More games will continue to be added as the project grows.

> Ultimately, the aim is to build a **complete multi-game platform** where users can enjoy several classic games from a single **Web or Android application**.

---

## 🤝 Contributing

```mermaid
gitGraph
    commit id: "Initial commit"
    branch feature/new-game
    checkout feature/new-game
    commit id: "Add game scaffold"
    commit id: "Implement core logic"
    checkout main
    merge feature/new-game id: "Merge PR"
    commit id: "Release v0.2"
```

1. 🍴 Fork the repo
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingGame`)
3. 💾 Commit your changes (`git commit -m 'feat: add my new game'`)
4. 📤 Push to the branch (`git push origin feature/AmazingGame`)
5. 🔁 Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👥 Contributors

> 💡 The full task breakdown for the upcoming **Flutter + Firebase application** lives in [`APP_DEVELOPMENT.md`](./APP_DEVELOPMENT.md).

<table align="center">
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/Subhadip-Paul2006">
        <img src="https://github.com/Subhadip-Paul2006.png" width="100" alt="Subhadip Paul"/><br/>
        <sub><b>Subhadip Paul</b></sub>
      </a><br/>
      🧑‍✈️ <em>Lead Developer</em><br/>
      Architecture · Firebase · DevOps
    </td>
    <td align="center" width="33%">
      <img src="https://avatars.githubusercontent.com/u/0?v=4" width="100" alt="Abhishek"/><br/>
      <sub><b>Abhishek</b></sub><br/>
      🎨 <em>Frontend Engineer</em><br/>
      Flutter UI · Animations · Game Shells
    </td>
    <td align="center" width="33%">
      <img src="https://avatars.githubusercontent.com/u/0?v=4" width="100" alt="Samhita"/><br/>
      <sub><b>Samhita</b></sub><br/>
      🧪 <em>UI/UX & QA Lead</em><br/>
      Design · Logic Port · Testing
    </td>
  </tr>
</table>

### Contribution Breakdown

| Contributor | Role | Primary Focus | Games Worked On |
|------------|------|---------------|-----------------|
| 🧑‍✈️ **Subhadip Paul** | Lead Developer | Architecture, Firebase backend, DevOps, code review | Tic Tac Toe · Snake · Hangman · MineSneeker · Rock Paper Scissors · Tetris |
| 🎨 **Abhishek** | Frontend Engineer | Flutter UI, animations, game UI shells, navigation | Tic Tac Toe · Snake · Flappy Bird · Pong |
| 🧪 **Samhita** | UI/UX & QA Lead | Design system, game logic ports, QA, localization | Flappy Bird |

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Subhadip-Paul2006">Subhadip Paul</a>, Abhishek &amp; Samhita.
</p>
