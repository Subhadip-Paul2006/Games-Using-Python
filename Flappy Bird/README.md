# 🐦 Flappy Bird Game (Python)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyGame-005F0F?style=for-the-badge&logo=python&logoColor=white" alt="PyGame"/>
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge" alt="Status"/>
</p>

A simple **Flappy Bird clone** built using **Python and Pygame** — with smooth animations, coin pickups, multiple sound effects, and authentic one-tap physics.

---

## 🎮 What is Flappy Bird?

> Tap **SPACE** to flap. Navigate the bird through endless pipes without crashing. Collect coins between pipes for bonus points. Survive as long as possible to set a new high score.

---

## 🌟 Features

- 🐤 Smooth bird flapping animation (wing up / wing down state)
- 🎵 Five distinct sound effects (flap, point, hit, die, swoosh)
- 💥 Pixel-perfect collision detection
- 🪙 Random coin pickups worth **+5 points**
- ☁️ Parallax-scrolling clouds
- 🚧 Procedurally generated pipe heights
- 📈 Real-time score tracking
- 🎮 Classic Flappy Bird one-tap mechanics

---

## 🕹️ Game Loop Overview

```mermaid
flowchart TD
    Start([🚀 Start Game]) --> Init[Initialize PyGame + Load Sounds/Sprites]
    Init --> Idle{Bird Idle on Start Screen?}
    Idle -- "Press SPACE" --> Play[Begin Gameplay]
    Play --> Gravity[Apply Gravity + Move Pipes Left]
    Gravity --> Collide{Collision with Pipe / Floor / Ceiling?}
    Collide -- "Yes" --> Death[Play Hit + Die Sound]
    Death --> Over[Show YOU LOSE + Final Score]
    Over --> Wait[Wait 5 seconds]
    Wait --> Exit([❌ Exit Process])

    Collide -- "No" --> Coin{Coin Collision?}
    Coin -- "Yes" --> Score[+5 Bonus, Hide Coin]
    Coin -- "No" --> Pass{Passed Pipe?}
    Pass -- "Yes" --> AddScore[+1 Score, Play Point Sound]
    Pass -- "No" --> Render
    Score --> Render[Render Frame]
    AddScore --> Render
    Render --> Gravity
```

---

## 🐦 Bird Physics

```mermaid
sequenceDiagram
    participant User
    participant Bird
    participant Game

    User->>Game: Press SPACE
    Game->>Bird: velocity = -7  (instant flap up)
    Note over Bird: gravity = +0.4 / frame

    loop Every Frame
        Bird->>Bird: velocity += gravity
        Bird->>Bird: bird_y += velocity
    end

    User->>Game: Press SPACE again
    Game->>Bird: velocity = -7  (re-flap)
```

---

## 🌐 World Rendering Pipeline

```mermaid
flowchart LR
    A[Clear Screen: Sky Blue] --> B[Draw Clouds]
    B --> C[Draw Top Pipe]
    C --> D[Draw Bottom Pipe]
    D --> E{Coin Visible?}
    E -- Yes --> F[Draw Coin Sprite]
    E -- No --> G[Skip]
    F --> H[Draw Bird Up/Down]
    G --> H
    H --> I[Draw Score HUD]
    I --> J[Optional Start/Lose Overlay]
    J --> K[pygame.display.update]
```

---

## 📁 Files

| File | Purpose |
|------|---------|
| `Flappy_Bird.py` | 🎮 Main game file — full game loop |
| `Test1.py` | 🧪 Experimental / prototype script |
| `flappy_up.png` | 🐤 Bird sprite (wings up) |
| `flappy_down.png` | 🐤 Bird sprite (wings down) |
| `coin.png` | 🪙 Collectible coin sprite |
| `flap.wav` | 🔊 Wing flap sound |
| `point.wav` | 🔊 Score + coin pickup chime |
| `hit.wav` | 🔊 Collision impact |
| `die.wav` | 🔊 Game-over melody |
| `swoosh.wav` | 🔊 Start-screen transition |
| `requirements.txt` | 📦 Dependency list |

---

## 🗂️ Project Structure

```text
Flappy Bird/
│
├── Flappy_Bird.py        # 🎮 Main game file
├── Test1.py              # 🧪 Test / prototype file
│
├── flappy_up.png         # 🐤 Bird sprite — wings up
├── flappy_down.png       # 🐤 Bird sprite — wings down
├── coin.png              # 🪙 Coin sprite
│
├── flap.wav              # 🔊 Flap sound
├── point.wav             # 🔊 Point / coin sound
├── hit.wav               # 🔊 Hit pipe sound
├── die.wav               # 🔊 Death sound
├── swoosh.wav            # 🔊 Start swoosh
│
├── requirements.txt      # 📦 Dependencies
└── README.md             # 📖 You are here
```

---

## ⚙️ Game Constants

```mermaid
classDiagram
    class GameConfig {
        +int WIDTH = 720
        +int HEIGHT = 480
        +float gravity = 0.4
        +int flap_velocity = -7
        +int pipe_width = 60
        +int pipe_gap = 150
        +int pipe_speed = 3
        +int FPS = 60
        +float coin_spawn_chance = 0.8
    }
```

---

## 🛠 Requirements

- 🐍 **Python 3.14** (or compatible 3.x)
- 🎮 **Pygame** library

```bash
pip install pygame
```

---

## ▶ How to Run

1. 📂 Navigate to the **Flappy Bird** folder.
2. 📦 Install pygame:
   ```bash
   pip install pygame
   ```
3. 🚀 Launch the game:
   ```bash
   python Flappy_Bird.py
   ```

---

## 🎮 Controls

| Action | Key |
|--------|-----|
| 🪶 Flap (Start / Jump) | <kbd>Space</kbd> |
| ❌ Quit (close window) | Window close button |

---

## 📊 Scoring Rules

```mermaid
pie title Score Sources
    "Passing Pipes (+1)" : 1
    "Collecting Coins (+5)" : 5
```

| Event | Points |
|-------|:------:|
| Pass a pipe | **+1** |
| Collect a coin | **+5** |
| Collide | **Game Over** |

---

## 🧩 Architecture Layers

```mermaid
flowchart TB
    subgraph Presentation["🎨 Presentation Layer"]
        BirdSprite[Bird Sprite Renderer]
        PipeRenderer[Pipe Renderer]
        CoinRenderer[Coin Renderer]
        HUDRenderer[HUD Renderer]
    end

    subgraph Logic["⚙️ Game Logic"]
        Physics[Bird Physics]
        Spawner[Pipe & Coin Spawner]
        Collision[Collision Detector]
        ScoreManager[Score Manager]
    end

    subgraph IO["🔊 Audio / Input"]
        SoundEngine[Sound Mixer]
        EventLoop[Event Poller]
    end

    Physics --> BirdSprite
    Spawner --> PipeRenderer
    Spawner --> CoinRenderer
    Collision --> ScoreManager
    EventLoop --> Physics
    SoundEngine -.-> BirdSprite
```

---

## 🔮 Future Improvements

- 🏆 Persistent high-score saving (JSON or DB)
- 🌈 Day / night cycle
- 🎨 Multiple bird skins
- 🚧 Difficulty modes (pipe speed, gap size)
- 📱 Touch / mobile input support

---

## 👨‍💻 Contributors

- **Abhishek Dutta**
- **Samhita Mondal**

---

<p align="center">
  Made with ❤️ and a lot of <kbd>SPACE</kbd> presses.
</p>
