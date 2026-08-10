"""
╔══════════════════════════════════════════════════════╗
║         MINESWEEPER  –  Modern Python Edition        ║
║  A polished Tkinter Minesweeper with:                ║
║   • Animated tiles & explosions                      ║
║   • HUD (mines counter, timer, emoji button)         ║
║   • Sound effects (pygame, with graceful fallback)   ║
║   • Dark Mode toggle                                 ║
║   • PostgreSQL high-score system                     ║
║   • Player name + result screen                      ║
╚══════════════════════════════════════════════════════╝

Usage:  python main.py
Requires:
    pip install pygame          (optional – game works without it)
    pip install psycopg2-binary  (optional – scores fall back to JSON)
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import sys
import os
import json
import time
import threading

# ── Database manager (PostgreSQL) ───────────────────────────────────────────
from db_manager import DatabaseManager

# ── Optional pygame for sound ───────────────────────────────────────────────
try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# ── Optional urllib for sound download ──────────────────────────────────────
try:
    from urllib.request import urlretrieve
    URLLIB_AVAILABLE = True
except Exception:
    URLLIB_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════
#  COLOUR PALETTES
# ═══════════════════════════════════════════════════════════════════════════
LIGHT_PALETTE = {
    "bg":             "#263238",   # Window / board background
    "panel":          "#37474F",   # HUD / panel backgrounds
    "tile_hidden":    "#546E7A",   # Unrevealed tile face
    "tile_hover":     "#607D8B",   # Tile hover highlight
    "tile_revealed":  "#ECEFF1",   # Revealed safe tile
    "tile_mine":      "#C62828",   # Mine explosion tile
    "tile_flag_mine": "#F9A825",   # Correctly flagged mine (win)
    "tile_wrong_flag":"#880E4F",   # Wrong flag tile
    "tile_safe_mine": "#2E7D32",   # Mine that was flagged correctly at win
    "btn_bg":         "#546E7A",   # General button colour
    "btn_hover":      "#78909C",   # Button hover
    "btn_text":       "#FFFFFF",
    "hud_text":       "#ECEFF1",
    "title_text":     "#80DEEA",
    "subtitle_text":  "#B0BEC5",
    "menu_bg":        "#1C2B35",
    "number": {
        "1": "#1565C0",  # Blue
        "2": "#2E7D32",  # Green
        "3": "#C62828",  # Red
        "4": "#4A148C",  # Purple
        "5": "#6D4C41",  # Brown
        "6": "#00838F",  # Cyan
        "7": "#212121",  # Black
        "8": "#757575",  # Grey
        "0": "#ECEFF1",  # Empty (blank)
    },
}

DARK_PALETTE = {
    "bg":             "#0D1117",
    "panel":          "#161B22",
    "tile_hidden":    "#21262D",
    "tile_hover":     "#30363D",
    "tile_revealed":  "#2D333B",
    "tile_mine":      "#B91C1C",
    "tile_flag_mine": "#D97706",
    "tile_wrong_flag":"#7C3AED",
    "tile_safe_mine": "#059669",
    "btn_bg":         "#21262D",
    "btn_hover":      "#30363D",
    "btn_text":       "#C9D1D9",
    "hud_text":       "#C9D1D9",
    "title_text":     "#58A6FF",
    "subtitle_text":  "#8B949E",
    "menu_bg":        "#010409",
    "number": {
        "1": "#58A6FF",
        "2": "#3FB950",
        "3": "#F85149",
        "4": "#BC8CFF",
        "5": "#D29922",
        "6": "#39C5CF",
        "7": "#C9D1D9",
        "8": "#6E7681",
        "0": "#2D333B",
    },
}

# ═══════════════════════════════════════════════════════════════════════════
#  GAME LOGIC  (all original algorithms preserved, wrapped in a class)
# ═══════════════════════════════════════════════════════════════════════════
class GameLogic:
    """Pure game-logic layer – no Tkinter references."""

    # Difficulty presets: (rows, cols, mine_probability_denominator)
    DIFFICULTIES = {
        "Easy":   (8,  16, 6),   # ~16% mines
        "Medium": (12, 24, 5),   # ~20% mines
        "Hard":   (16, 30, 4),   # ~25% mines
    }

    @staticmethod
    def generate_board(rows: int, cols: int, mine_prob_denom: int):
        """Return (board, mine_count).  'M'=mine, 'E'=empty."""
        choices = ["E"] * (mine_prob_denom - 1) + ["M"]
        board = []
        mine_count = 0
        for _ in range(rows):
            row = []
            for _ in range(cols):
                cell = random.choice(choices)
                if cell == "M":
                    mine_count += 1
                row.append(cell)
            board.append(row)
        return board, mine_count

    @staticmethod
    def build_number_board(raw_board):
        """Overlay mine-counts onto a copy of the board.  'M' stays 'M';
        safe cells become '0'..'8' strings."""
        rows = len(raw_board)
        cols = len(raw_board[0])
        vis = [["0"] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if raw_board[r][c] == "M":
                    vis[r][c] = "M"
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and raw_board[nr][nc] != "M":
                                vis[nr][nc] = str(int(vis[nr][nc]) + 1)
        return vis

    @staticmethod
    def dfs_reveal(row, col, game_board, number_board, visited, to_reveal):
        """Flood-fill reveal of zero tiles; collects indices into `to_reveal`."""
        rows = len(game_board)
        cols = len(game_board[0])
        visited[row][col] = 1
        game_board[row][col] = "B"
        idx = cols * row + col
        to_reveal.add(idx)
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                    if number_board[nr][nc] == "0":
                        GameLogic.dfs_reveal(nr, nc, game_board, number_board, visited, to_reveal)
                    else:
                        game_board[nr][nc] = number_board[nr][nc]
                        to_reveal.add(cols * nr + nc)

    @staticmethod
    def check_win(mine_count, game_board, number_board):
        """Return True if all non-mine cells have been revealed."""
        unrevealed = sum(
            1 for r in range(len(game_board))
            for c in range(len(game_board[0]))
            if game_board[r][c] == "E"
        )
        return unrevealed == mine_count

    @staticmethod
    def make_game_board(raw_board):
        return [["E"] * len(raw_board[0]) for _ in range(len(raw_board))]

    @staticmethod
    def make_visited(raw_board):
        return [[0] * len(raw_board[0]) for _ in range(len(raw_board))]

    @staticmethod
    def make_coordinates(raw_board):
        cols = len(raw_board[0])
        return {r * cols + c: (r, c)
                for r in range(len(raw_board))
                for c in range(cols)}


# ═══════════════════════════════════════════════════════════════════════════
#  SOUND MANAGER
# ═══════════════════════════════════════════════════════════════════════════
class SoundManager:
    """
    Loads and plays WAV sound effects via pygame.mixer.
    Falls back to a no-op silently if pygame is missing or files not found.

    Sound files are stored in  <script_dir>/assets/sounds/
    On first run the manager tries to download free CC0 sounds automatically.
    """

    SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")

    # Public-domain / CC0 sound proxies (short wav clips from opengameart/freesound CDNs)
    DOWNLOAD_URLS = {
        "click":     "https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3",
        "flag":      "https://assets.mixkit.co/active_storage/sfx/270/270-preview.mp3",
        "unflag":    "https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3",
        "explosion": "https://assets.mixkit.co/active_storage/sfx/1929/1929-preview.mp3",
        "win":       "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3",
        "button":    "https://assets.mixkit.co/active_storage/sfx/2204/2204-preview.mp3",
    }

    def __init__(self):
        self._sounds = {}
        self._muted = False
        self._enabled = PYGAME_AVAILABLE
        if self._enabled:
            os.makedirs(self.SOUND_DIR, exist_ok=True)
            self._try_download_sounds()
            self._load_sounds()

    # ── Download ────────────────────────────────────────────────────────────
    def _try_download_sounds(self):
        if not URLLIB_AVAILABLE:
            return
        for name, url in self.DOWNLOAD_URLS.items():
            ext = url.split(".")[-1].split("?")[0]  # mp3 or wav
            path = os.path.join(self.SOUND_DIR, f"{name}.{ext}")
            if not os.path.exists(path):
                try:
                    urlretrieve(url, path)
                except Exception:
                    pass  # Silent fail – game runs without sounds

    # ── Load ────────────────────────────────────────────────────────────────
    def _load_sounds(self):
        if not self._enabled:
            return
        for name in self.DOWNLOAD_URLS:
            for ext in ("wav", "mp3", "ogg"):
                path = os.path.join(self.SOUND_DIR, f"{name}.{ext}")
                if os.path.exists(path):
                    try:
                        self._sounds[name] = pygame.mixer.Sound(path)
                        self._sounds[name].set_volume(0.5)
                        break
                    except Exception:
                        pass

    # ── Play ────────────────────────────────────────────────────────────────
    def play(self, name: str):
        if self._enabled and not self._muted and name in self._sounds:
            try:
                self._sounds[name].play()
            except Exception:
                pass

    def toggle_mute(self):
        self._muted = not self._muted
        return self._muted

    @property
    def muted(self):
        return self._muted


# ═══════════════════════════════════════════════════════════════════════════
#  SCORE MANAGER
# ═══════════════════════════════════════════════════════════════════════════
class ScoreManager:
    """Persists best times (seconds) per difficulty in scores.json."""

    SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")

    def __init__(self):
        self._scores = self._load()

    def _load(self):
        if os.path.exists(self.SCORE_FILE):
            try:
                with open(self.SCORE_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"Easy": None, "Medium": None, "Hard": None}

    def _save(self):
        try:
            with open(self.SCORE_FILE, "w") as f:
                json.dump(self._scores, f, indent=2)
        except Exception:
            pass

    def get_best(self, difficulty: str):
        return self._scores.get(difficulty)

    def submit(self, difficulty: str, elapsed: float):
        """Update best time if this run is faster. Returns True if new record."""
        current = self._scores.get(difficulty)
        if current is None or elapsed < current:
            self._scores[difficulty] = round(elapsed, 1)
            self._save()
            return True
        return False

    def format_time(self, seconds) -> str:
        if seconds is None:
            return "–"
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION  (root + screen manager)
# ═══════════════════════════════════════════════════════════════════════════
class MinesweeperApp:
    """
    Manages the Tk root window and switches between screens.
    Owns shared services: SoundManager, ScoreManager, DatabaseManager,
    and the current player name.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.root.configure(bg=LIGHT_PALETTE["bg"])

        # ── Centre window ───────────────────────────────────────────────
        self._centre_window(420, 340)

        # ── Shared services ─────────────────────────────────────────────
        self.sound = SoundManager()
        self.scores = ScoreManager()        # JSON fallback
        self.db = DatabaseManager()          # PostgreSQL (graceful fallback)
        self._dark_mode = False
        self._current_screen = None
        self.player_name = ""               # Set by WelcomeScreen

        # ── Intercept close ─────────────────────────────────────────────
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # ── Load fonts (system fonts; no external deps needed) ──────────
        self._load_fonts()

        # ── Show welcome screen first ───────────────────────────────────
        self.show_welcome()
        self.root.mainloop()

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _centre_window(self, w: int, h: int):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _load_fonts(self):
        available = list(tkfont.families())
        pref = ["Segoe UI", "Helvetica Neue", "Arial", "sans-serif"]
        self.font_ui = next((f for f in pref if f in available), "TkDefaultFont")

    @property
    def palette(self):
        return DARK_PALETTE if self._dark_mode else LIGHT_PALETTE

    def toggle_dark_mode(self):
        self._dark_mode = not self._dark_mode
        # Re-show current menu to repaint everything
        self.show_menu()

    def _on_close(self):
        self.db.close()
        self.root.destroy()
        sys.exit()

    # ── Screen switching ────────────────────────────────────────────────────
    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_welcome(self):
        """Show the welcome / player-name screen."""
        self._clear()
        self._current_screen = WelcomeScreen(self)

    def show_menu(self):
        """Show the difficulty-selection menu."""
        self._clear()
        self._current_screen = MainMenuScreen(self)

    def show_game(self, difficulty: str):
        """Start a game with the currently set player_name."""
        self._clear()
        self._current_screen = GameScreen(self, difficulty, self.player_name)


# ═══════════════════════════════════════════════════════════════════════════
#  WELCOME SCREEN  (player name entry)
# ═══════════════════════════════════════════════════════════════════════════
class WelcomeScreen:
    """
    First screen shown on launch.  The player enters their name,
    then proceeds to the difficulty-selection menu.
    """

    def __init__(self, app: MinesweeperApp):
        self.app = app
        self.root = app.root
        self.p = app.palette

        self.root.configure(bg=self.p["menu_bg"])
        self.root.resizable(False, False)
        self._resize(420, 360)
        self._build()

    def _resize(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        p = self.p
        outer = tk.Frame(self.root, bg=p["menu_bg"])
        outer.pack(fill="both", expand=True, padx=30, pady=20)

        # ── Title ─────────────────────────────────────────────────────────
        tk.Label(
            outer,
            text="💣 MINESWEEPER 💣",
            font=(self.app.font_ui, 26, "bold"),
            fg=p["title_text"],
            bg=p["menu_bg"],
        ).pack(pady=(20, 6))

        tk.Label(
            outer,
            text="Welcome, Sweeper!",
            font=(self.app.font_ui, 12),
            fg=p["subtitle_text"],
            bg=p["menu_bg"],
        ).pack(pady=(0, 24))

        # ── Name label ────────────────────────────────────────────────────
        tk.Label(
            outer,
            text="Enter Your Name",
            font=(self.app.font_ui, 11, "bold"),
            fg=p["hud_text"],
            bg=p["menu_bg"],
        ).pack(pady=(0, 6))

        # ── Name entry ────────────────────────────────────────────────────
        self._name_var = tk.StringVar()
        entry = tk.Entry(
            outer,
            textvariable=self._name_var,
            font=(self.app.font_ui, 14),
            fg=p["btn_text"],
            bg=p["panel"],
            insertbackground=p["title_text"],
            relief="flat",
            bd=0,
            justify="center",
            width=20,
        )
        entry.pack(pady=(0, 20), ipady=8)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self._start())

        # ── Start button ──────────────────────────────────────────────────
        start_btn = tk.Button(
            outer,
            text="🚀  Start Game",
            font=(self.app.font_ui, 13, "bold"),
            fg=p["btn_text"],
            bg="#2E7D32",
            activebackground="#388E3C",
            activeforeground=p["btn_text"],
            relief="flat",
            bd=0,
            padx=24,
            pady=10,
            cursor="hand2",
            command=self._start,
        )
        start_btn.pack(pady=5, fill="x")

        def on_enter(e):
            start_btn.configure(bg="#388E3C")
        def on_leave(e):
            start_btn.configure(bg="#2E7D32")
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

        # ── DB status indicator ──────────────────────────────────────────
        db_status = "✅ Database Connected" if self.app.db.available else "⚠️ DB Offline — scores saved locally"
        db_color = "#2E7D32" if self.app.db.available else "#F57F17"
        tk.Label(
            outer,
            text=db_status,
            font=(self.app.font_ui, 8),
            fg=db_color,
            bg=p["menu_bg"],
        ).pack(pady=(14, 0))

    def _start(self):
        """Validate name and move to difficulty menu."""
        name = self._name_var.get().strip()
        if not name:
            name = "Player"  # Default fallback
        self.app.player_name = name
        self.app.sound.play("button")
        self.app.show_menu()


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN MENU SCREEN
# ═══════════════════════════════════════════════════════════════════════════
class MainMenuScreen:
    """
    Displays:
      • Animated title "MINESWEEPER"
      • Subtitle "Select Difficulty"
      • Easy / Medium / Hard buttons with hover effects
      • Dark-mode toggle
      • Best scores table
    """

    def __init__(self, app: MinesweeperApp):
        self.app = app
        self.root = app.root
        self.p = app.palette

        self.root.configure(bg=self.p["menu_bg"])
        self.root.resizable(False, False)
        self._resize_window(420, 400)

        self._build()
        self._animate_title()

    def _resize_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── Build ────────────────────────────────────────────────────────────────
    def _build(self):
        p = self.p

        # ── Outer frame ──────────────────────────────────────────────────
        outer = tk.Frame(self.root, bg=p["menu_bg"])
        outer.pack(fill="both", expand=True, padx=30, pady=20)

        # ── Title (animated) ─────────────────────────────────────────────
        self._title_var = tk.StringVar(value="💣 MINESWEEPER 💣")
        self._title_lbl = tk.Label(
            outer,
            textvariable=self._title_var,
            font=(self.app.font_ui, 26, "bold"),
            fg=p["title_text"],
            bg=p["menu_bg"],
        )
        self._title_lbl.pack(pady=(10, 4))

        # ── Player greeting ──────────────────────────────────────────────
        greeting = f"👋 Welcome, {self.app.player_name}!" if self.app.player_name else "Select Difficulty"
        tk.Label(
            outer,
            text=greeting,
            font=(self.app.font_ui, 12),
            fg=p["subtitle_text"],
            bg=p["menu_bg"],
        ).pack(pady=(0, 4))

        tk.Label(
            outer,
            text="Select Difficulty",
            font=(self.app.font_ui, 10),
            fg=p["subtitle_text"],
            bg=p["menu_bg"],
        ).pack(pady=(0, 14))

        # ── Difficulty buttons ────────────────────────────────────────────
        btn_frame = tk.Frame(outer, bg=p["menu_bg"])
        btn_frame.pack(pady=5)

        for label, diff, emoji in [
            ("🟢  Easy",   "Easy",   "#2E7D32"),
            ("🟡  Medium", "Medium", "#F57F17"),
            ("🔴  Hard",   "Hard",   "#C62828"),
        ]:
            self._make_menu_btn(btn_frame, label, diff, emoji)

        # ── Divider ───────────────────────────────────────────────────────
        tk.Frame(outer, height=2, bg=p["panel"]).pack(fill="x", pady=15)

        # ── Best scores (from DB first, JSON fallback) ─────────────────────
        tk.Label(
            outer,
            text="🏆  Best Times",
            font=(self.app.font_ui, 11, "bold"),
            fg=p["subtitle_text"],
            bg=p["menu_bg"],
        ).pack(pady=(0, 6))

        score_frame = tk.Frame(outer, bg=p["menu_bg"])
        score_frame.pack()

        for i, diff in enumerate(["Easy", "Medium", "Hard"]):
            # Try DB first, fall back to JSON
            db_best = self.app.db.get_best_score(diff)
            if db_best:
                holder = db_best["player_name"]
                best_secs = db_best["time_seconds"]
                time_str = DatabaseManager.format_time(best_secs)
                label_str = f"{time_str} ({holder})"
                color = p["title_text"]
            else:
                json_best = self.app.scores.get_best(diff)
                time_str = self.app.scores.format_time(json_best)
                label_str = time_str
                color = p["title_text"] if json_best else p["subtitle_text"]

            tk.Label(
                score_frame,
                text=f"{diff}:",
                font=(self.app.font_ui, 10),
                fg=p["subtitle_text"],
                bg=p["menu_bg"],
                width=8,
                anchor="e",
            ).grid(row=i, column=0, padx=4, pady=2)
            tk.Label(
                score_frame,
                text=label_str,
                font=(self.app.font_ui, 10, "bold"),
                fg=color,
                bg=p["menu_bg"],
                width=16,
                anchor="w",
            ).grid(row=i, column=1, padx=4, pady=2)

        # ── DB status ─────────────────────────────────────────────────────
        if not self.app.db.available:
            tk.Label(
                outer,
                text="⚠️ DB Offline — using local scores",
                font=(self.app.font_ui, 8),
                fg="#F57F17",
                bg=p["menu_bg"],
            ).pack(pady=(4, 0))

        # ── Bottom controls ───────────────────────────────────────────────
        ctrl_frame = tk.Frame(outer, bg=p["menu_bg"])
        ctrl_frame.pack(pady=12)

        dark_label = "☀️ Light Mode" if self.app._dark_mode else "🌙 Dark Mode"
        self._make_icon_btn(ctrl_frame, dark_label, self.app.toggle_dark_mode, side="left")

        sound_label = "🔇 Sound Off" if self.app.sound.muted else "🔊 Sound On"
        self._sound_btn_var = tk.StringVar(value=sound_label)
        self._make_icon_btn(
            ctrl_frame, None, self._toggle_sound, side="left",
            textvariable=self._sound_btn_var
        )

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _make_menu_btn(self, parent, text, diff, accent):
        p = self.p

        btn = tk.Button(
            parent,
            text=text,
            font=(self.app.font_ui, 13, "bold"),
            fg=p["btn_text"],
            bg=p["btn_bg"],
            activebackground=p["btn_hover"],
            activeforeground=p["btn_text"],
            relief="flat",
            bd=0,
            padx=24,
            pady=10,
            cursor="hand2",
            command=lambda d=diff: self._start_game(d),
        )
        btn.pack(pady=5, fill="x")

        # Hover effects
        def on_enter(e, b=btn):
            b.configure(bg=accent)
        def on_leave(e, b=btn):
            b.configure(bg=p["btn_bg"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _make_icon_btn(self, parent, text=None, cmd=None, side="left", textvariable=None):
        p = self.p
        kwargs = dict(
            font=(self.app.font_ui, 9),
            fg=p["subtitle_text"],
            bg=p["menu_bg"],
            activebackground=p["menu_bg"],
            activeforeground=p["title_text"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=cmd,
            padx=8,
            pady=4,
        )
        if textvariable:
            kwargs["textvariable"] = textvariable
        else:
            kwargs["text"] = text

        btn = tk.Button(parent, **kwargs)
        btn.pack(side=side, padx=6)

    def _start_game(self, difficulty: str):
        self.app.sound.play("button")
        self.app.show_game(difficulty)

    def _toggle_sound(self):
        muted = self.app.sound.toggle_mute()
        self._sound_btn_var.set("🔇 Sound Off" if muted else "🔊 Sound On")

    # ── Title animation ───────────────────────────────────────────────────────
    _TITLE_FRAMES = [
        "💣 MINESWEEPER 💣",
        "💥 MINESWEEPER 💥",
    ]
    _anim_idx = 0

    def _animate_title(self):
        if not hasattr(self, "_title_lbl") or not self._title_lbl.winfo_exists():
            return
        self._title_var.set(self._TITLE_FRAMES[self._anim_idx % 2])
        self._anim_idx += 1
        self.root.after(900, self._animate_title)


# ═══════════════════════════════════════════════════════════════════════════
#  GAME SCREEN
# ═══════════════════════════════════════════════════════════════════════════
class GameScreen:
    """
    The main game view:
      • HUD bar  (mines counter | timer | emoji restart button | mute | menu)
      • Grid of tile buttons
      • Handles left-click (reveal) and right-click (flag)
      • Tile reveal, expansion, explosion & flag animations
    """

    # Number colours (classic Minesweeper palette)
    NUMBER_COLORS = {
        "1": "#1565C0", "2": "#2E7D32", "3": "#C62828",
        "4": "#4A148C", "5": "#6D4C41", "6": "#00838F",
        "7": "#212121", "8": "#757575",
    }

    def __init__(self, app: MinesweeperApp, difficulty: str, player_name: str = "Player"):
        self.app = app
        self.root = app.root
        self.p = app.palette
        self.difficulty = difficulty
        self.player_name = player_name

        # ── Game state ───────────────────────────────────────────────────
        rows, cols, denom = GameLogic.DIFFICULTIES[difficulty]
        self.raw_board, self.mine_count = GameLogic.generate_board(rows, cols, denom)
        self.number_board = GameLogic.build_number_board(self.raw_board)
        self.game_board   = GameLogic.make_game_board(self.raw_board)
        self.visited      = GameLogic.make_visited(self.raw_board)
        self.coordinates  = GameLogic.make_coordinates(self.raw_board)
        self.rows, self.cols = rows, cols

        self.flagged = set()           # indices of flagged tiles
        self.remaining_mines = self.mine_count
        self.game_over = False
        self.first_click = True

        # ── Timer ────────────────────────────────────────────────────────
        self._start_time = None
        self._elapsed = 0.0
        self._timer_running = False

        # ── HUD vars ────────────────────────────────────────────────────
        self._mines_var = tk.StringVar(value=f"💣 {self.remaining_mines:03d}")
        self._time_var  = tk.StringVar(value="⏱ 00:00")
        self._face_var  = tk.StringVar(value="🙂")

        # ── Build UI ─────────────────────────────────────────────────────
        self.root.configure(bg=self.p["bg"])
        self._fit_window()
        self._build()

    # ── Window sizing ────────────────────────────────────────────────────────
    def _fit_window(self):
        TILE_W = 36
        TILE_H = 36
        HUD_H  = 60
        BOTTOM_H = 44
        PADDING  = 20

        w = self.cols * TILE_W + PADDING * 2
        h = self.rows * TILE_H + HUD_H + BOTTOM_H + PADDING * 2

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── Build ────────────────────────────────────────────────────────────────
    def _build(self):
        p = self.p

        # ── HUD ──────────────────────────────────────────────────────────
        hud = tk.Frame(self.root, bg=p["panel"], pady=8)
        hud.pack(fill="x", padx=0, pady=0)

        tk.Label(
            hud, textvariable=self._mines_var,
            font=(self.app.font_ui, 14, "bold"),
            fg="#EF5350", bg=p["panel"], width=10, anchor="w"
        ).pack(side="left", padx=(14, 0))

        # ── Emoji / restart button ─────────────────────────────────────
        face_btn = tk.Button(
            hud,
            textvariable=self._face_var,
            font=(self.app.font_ui, 18),
            bg=p["btn_bg"],
            activebackground=p["btn_hover"],
            fg=p["btn_text"],
            relief="flat", bd=0,
            cursor="hand2",
            padx=6, pady=2,
            command=self._restart,
        )
        face_btn.pack(side="left", expand=True)
        self._add_hover(face_btn, p["btn_hover"], p["btn_bg"])

        tk.Label(
            hud, textvariable=self._time_var,
            font=(self.app.font_ui, 14, "bold"),
            fg="#42A5F5", bg=p["panel"], width=10, anchor="e"
        ).pack(side="right", padx=(0, 14))

        # ── Grid ─────────────────────────────────────────────────────────
        grid_frame = tk.Frame(self.root, bg=p["bg"])
        grid_frame.pack(padx=10, pady=8)

        self.buttons = []
        for r in range(self.rows):
            for c in range(self.cols):
                idx = r * self.cols + c
                btn = tk.Button(
                    grid_frame,
                    text="",
                    width=2, height=1,
                    font=(self.app.font_ui, 11, "bold"),
                    fg=p["btn_text"],
                    bg=p["tile_hidden"],
                    activebackground=p["tile_hover"],
                    relief="raised",
                    bd=2,
                    cursor="hand2",
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Button-1>",   lambda e, i=idx: self._on_left(i))
                btn.bind("<Button-3>",   lambda e, i=idx: self._on_right(i))
                btn.bind("<Enter>",      lambda e, b=btn: self._tile_hover_enter(b))
                btn.bind("<Leave>",      lambda e, b=btn: self._tile_hover_leave(b))
                self.buttons.append(btn)

        # ── Bottom bar ───────────────────────────────────────────────────
        bottom = tk.Frame(self.root, bg=p["bg"])
        bottom.pack(fill="x", padx=10, pady=(0, 8))

        self._make_ctrl_btn(bottom, "🔄 New Board", self._restart).pack(side="left", padx=4)
        self._make_ctrl_btn(bottom, "🏠 Main Menu", self.app.show_menu).pack(side="left", padx=4)

        sound_lbl = "🔇" if self.app.sound.muted else "🔊"
        self._sound_var = tk.StringVar(value=sound_lbl)
        mute_btn = self._make_ctrl_btn(bottom, None, self._toggle_sound, textvariable=self._sound_var)
        mute_btn.pack(side="right", padx=4)

        diff_colors = {"Easy": "#2E7D32", "Medium": "#F57F17", "Hard": "#C62828"}
        tk.Label(
            bottom,
            text=self.difficulty,
            font=(self.app.font_ui, 9, "bold"),
            fg=diff_colors.get(self.difficulty, p["subtitle_text"]),
            bg=p["bg"],
        ).pack(side="right", padx=8)

    # ── Control button factory ────────────────────────────────────────────────
    def _make_ctrl_btn(self, parent, text, cmd, textvariable=None):
        p = self.p
        kw = dict(
            font=(self.app.font_ui, 9, "bold"),
            fg=p["btn_text"],
            bg=p["btn_bg"],
            activebackground=p["btn_hover"],
            activeforeground=p["btn_text"],
            relief="flat", bd=0,
            cursor="hand2",
            padx=10, pady=5,
            command=cmd,
        )
        if textvariable:
            kw["textvariable"] = textvariable
        else:
            kw["text"] = text
        btn = tk.Button(parent, **kw)
        self._add_hover(btn, p["btn_hover"], p["btn_bg"])
        return btn

    # ── Hover helpers ──────────────────────────────────────────────────────────
    def _add_hover(self, widget, enter_color, leave_color):
        widget.bind("<Enter>", lambda e: widget.configure(bg=enter_color))
        widget.bind("<Leave>", lambda e: widget.configure(bg=leave_color))

    def _tile_hover_enter(self, btn):
        if btn["state"] != tk.DISABLED and btn["relief"] == "raised":
            btn.configure(bg=self.p["tile_hover"])

    def _tile_hover_leave(self, btn):
        if btn["state"] != tk.DISABLED and btn["relief"] == "raised":
            btn.configure(bg=self.p["tile_hidden"])

    # ── Timer ─────────────────────────────────────────────────────────────────
    def _start_timer(self):
        self._start_time = time.time()
        self._timer_running = True
        self._tick()

    def _tick(self):
        if not self._timer_running:
            return
        self._elapsed = time.time() - self._start_time
        m, s = divmod(int(self._elapsed), 60)
        self._time_var.set(f"⏱ {m:02d}:{s:02d}")
        self.root.after(500, self._tick)

    def _stop_timer(self):
        self._timer_running = False

    # ── Input handlers ────────────────────────────────────────────────────────
    def _on_left(self, idx: int):
        if self.game_over:
            return
        if idx in self.flagged:
            return  # Can't reveal a flagged tile
        if self.buttons[idx]["state"] == tk.DISABLED:
            return

        # Start timer on first actual click
        if self.first_click:
            self.first_click = False
            self._start_timer()

        r, c = self.coordinates[idx]
        cell = self.number_board[r][c]

        if cell == "M":
            # ── HIT A MINE ────────────────────────────────────────────
            self.app.sound.play("explosion")
            self._stop_timer()
            self.game_over = True
            self._face_var.set("😵")
            self._reveal_all_mines(triggered_idx=idx)
        else:
            self.app.sound.play("click")
            to_reveal = set()
            if cell == "0":
                # Flood-fill via DFS
                GameLogic.dfs_reveal(r, c, self.game_board, self.number_board, self.visited, to_reveal)
                self._animate_reveal_batch(sorted(to_reveal), idx)
            else:
                # Single number tile
                self.game_board[r][c] = cell
                self._reveal_tile(idx, cell, animated=True)

            # Check win after reveal
            if GameLogic.check_win(self.mine_count, self.game_board, self.number_board):
                self._on_win()

    def _on_right(self, idx: int):
        if self.game_over:
            return
        if self.buttons[idx]["state"] == tk.DISABLED:
            return

        btn = self.buttons[idx]

        if idx in self.flagged:
            # Un-flag
            self.app.sound.play("unflag")
            self.flagged.discard(idx)
            self.remaining_mines += 1
            self._mines_var.set(f"💣 {self.remaining_mines:03d}")
            btn.configure(text="", fg=self.p["btn_text"], bg=self.p["tile_hidden"], relief="raised")
        else:
            # Flag
            self.app.sound.play("flag")
            self.flagged.add(idx)
            self.remaining_mines -= 1
            self._mines_var.set(f"💣 {self.remaining_mines:03d}")
            # Flag animation: quick font pulse
            self._animate_flag(btn)

    # ── Reveal helpers ────────────────────────────────────────────────────────
    def _reveal_tile(self, idx: int, cell: str, animated: bool = False):
        btn = self.buttons[idx]
        p = self.p

        label = ""
        fg = p["btn_text"]
        bg = p["tile_revealed"]

        if cell == "M":
            label = "💣"
            bg = p["tile_mine"]
        elif cell in ("0", "B"):
            label = ""
            fg = p["tile_revealed"]
        else:
            label = cell
            # Use dark-mode-aware number colors from palette, falling back to class constant
            num_colors = p.get("number", self.NUMBER_COLORS)
            fg = num_colors.get(cell, p["btn_text"])

        if animated:
            # Quick flash: briefly show a lighter colour then settle
            original_bg = btn["bg"]
            btn.configure(bg="#80CBC4", relief="sunken", text=label, fg=fg, state=tk.DISABLED)
            self.root.after(80, lambda: btn.configure(bg=bg) if btn.winfo_exists() else None)
        else:
            btn.configure(text=label, fg=fg, bg=bg, relief="sunken", state=tk.DISABLED)

    def _animate_reveal_batch(self, indices: list, origin: int):
        """Cascade reveal: tiles closest to origin first."""
        if not indices:
            return

        # Sort by Manhattan distance from origin
        or_r, or_c = self.coordinates[origin]
        def dist(i):
            r, c = self.coordinates[i]
            return abs(r - or_r) + abs(c - or_c)

        sorted_indices = sorted(indices, key=dist)

        DELAY_PER_STEP = 18   # ms

        def reveal_step(group_start):
            group = sorted_indices[group_start:group_start + 4]
            for i in group:
                r, c = self.coordinates[i]
                cell = self.number_board[r][c]
                if cell == "0":
                    cell = "B"   # blank
                self._reveal_tile(i, cell, animated=True)
            next_start = group_start + 4
            if next_start < len(sorted_indices):
                self.root.after(DELAY_PER_STEP, lambda: reveal_step(next_start))

        reveal_step(0)

    def _animate_flag(self, btn: tk.Button):
        """Quick scale animation using font size."""
        original_font = (self.app.font_ui, 11, "bold")
        big_font      = (self.app.font_ui, 16, "bold")

        btn.configure(text="🚩", fg="#EF5350", bg=self.p["tile_hidden"],
                      font=big_font, relief="raised")
        self.root.after(120, lambda: btn.configure(font=original_font)
                        if btn.winfo_exists() else None)

    # ── Win / Loss ────────────────────────────────────────────────────────────
    def _on_win(self):
        self._stop_timer()
        self.game_over = True
        self._face_var.set("😎")
        self.app.sound.play("win")

        # Mark all unflagged mines as ✅
        for idx, (r, c) in self.coordinates.items():
            if self.number_board[r][c] == "M":
                btn = self.buttons[idx]
                btn.configure(text="✅", bg=self.p["tile_safe_mine"],
                              relief="sunken", state=tk.DISABLED)

        elapsed_int = int(self._elapsed)

        # ── Check if this is a new high score BEFORE inserting ────────
        is_new_hs = self.app.db.is_new_record(self.difficulty, elapsed_int)

        # ── Save score to PostgreSQL ──────────────────────────────────
        self.app.db.insert_score(
            self.player_name, self.difficulty, elapsed_int, "Win"
        )

        # ── Also update JSON fallback ─────────────────────────────────
        self.app.scores.submit(self.difficulty, self._elapsed)

        # ── Show result screen after a short delay ────────────────────
        self.root.after(
            400,
            lambda: self._show_result_screen(win=True, is_new_record=is_new_hs),
        )

    def _reveal_all_mines(self, triggered_idx: int):
        """Explode all mines with a ripple animation, then show dialog."""
        p = self.p
        all_mine_indices = [
            idx for idx, (r, c) in self.coordinates.items()
            if self.number_board[r][c] == "M"
        ]

        # Sort by distance from triggered mine for ripple
        tr_r, tr_c = self.coordinates[triggered_idx]
        def dist(i):
            r, c = self.coordinates[i]
            return abs(r-tr_r) + abs(c-tr_c)

        sorted_mines = sorted(all_mine_indices, key=dist)

        DELAY = 60  # ms between ripple waves

        def explode_step(step_idx):
            if step_idx >= len(sorted_mines):
                # Save loss to DB (time is recorded even on loss for stats)
                elapsed_int = int(self._elapsed) if self._elapsed > 0 else 0
                self.app.db.insert_score(
                    self.player_name, self.difficulty, elapsed_int, "Loss"
                )
                self.root.after(400, lambda: self._show_result_screen(win=False, is_new_record=False))
                return
            idx = sorted_mines[step_idx]
            btn = self.buttons[idx]
            # Correctly flagged mines
            if idx in self.flagged:
                btn.configure(text="✅", bg=p["tile_flag_mine"],
                              relief="sunken", state=tk.DISABLED)
            else:
                # Flash bright red then settle
                btn.configure(text="💣", bg="#FF5252", relief="sunken", state=tk.DISABLED)
                self.root.after(
                    DELAY // 2,
                    lambda b=btn: b.configure(bg=p["tile_mine"]) if b.winfo_exists() else None,
                )
            self.root.after(DELAY, lambda: explode_step(step_idx + 1))

        # Mark wrongly placed flags
        for idx in self.flagged:
            r, c = self.coordinates[idx]
            if self.number_board[r][c] != "M":
                self.buttons[idx].configure(text="❌", bg=p["tile_wrong_flag"],
                                            relief="sunken", state=tk.DISABLED)

        explode_step(0)

    def _show_result_screen(self, win: bool, is_new_record: bool = False):
        """
        Enhanced Result Screen showing:
          • Player Name
          • Player Time
          • Best Time for this difficulty (from DB)
          • 🏆 NEW HIGH SCORE! indicator
        Buttons: Play Again | Main Menu | Exit
        """
        p = self.p
        dialog = tk.Toplevel(self.root)
        dialog.title("Minesweeper — Results")
        dialog.resizable(False, False)
        dialog.configure(bg=p["panel"])
        dialog.grab_set()
        dialog.transient(self.root)

        # Centre over root
        self.root.update_idletasks()
        rx = self.root.winfo_x() + self.root.winfo_width()  // 2
        ry = self.root.winfo_y() + self.root.winfo_height() // 2
        dialog.geometry(f"+{rx - 180}+{ry - 130}")

        content = tk.Frame(dialog, bg=p["panel"], padx=30, pady=20)
        content.pack(fill="both", expand=True)

        # ── Status emoji + headline ───────────────────────────────────
        if win:
            headline = "😎 You Won!"
            hl_color = "#2E7D32"
        else:
            headline = "😵 Game Over!"
            hl_color = "#C62828"

        tk.Label(
            content, text=headline,
            font=(self.app.font_ui, 18, "bold"),
            fg=hl_color, bg=p["panel"],
        ).pack(pady=(0, 12))

        # ── NEW HIGH SCORE indicator ──────────────────────────────────
        if win and is_new_record:
            tk.Label(
                content, text="🏆 NEW HIGH SCORE! 🏆",
                font=(self.app.font_ui, 14, "bold"),
                fg="#F9A825", bg=p["panel"],
            ).pack(pady=(0, 10))

        # ── Info rows ─────────────────────────────────────────────────
        info_frame = tk.Frame(content, bg=p["panel"])
        info_frame.pack(pady=(0, 8))

        elapsed_fmt = self.app.scores.format_time(self._elapsed)

        info_rows = [
            ("Player",    self.player_name),
            ("Difficulty", self.difficulty),
            ("Your Time", elapsed_fmt if win else f"{elapsed_fmt} (Lost)"),
        ]

        # ── Best time from DB ─────────────────────────────────────────
        db_best = self.app.db.get_best_score(self.difficulty)
        if db_best:
            best_fmt = DatabaseManager.format_time(db_best["time_seconds"])
            holder = db_best["player_name"]
            info_rows.append(
                (f"Best ({self.difficulty})", f"{best_fmt}  — by {holder}")
            )
        else:
            # Fallback to JSON
            json_best = self.app.scores.get_best(self.difficulty)
            best_fmt = self.app.scores.format_time(json_best)
            info_rows.append(
                (f"Best ({self.difficulty})", best_fmt)
            )

        for i, (label, value) in enumerate(info_rows):
            tk.Label(
                info_frame, text=f"{label}:",
                font=(self.app.font_ui, 11),
                fg=p["subtitle_text"], bg=p["panel"],
                anchor="e", width=14,
            ).grid(row=i, column=0, padx=(0, 8), pady=3, sticky="e")
            tk.Label(
                info_frame, text=value,
                font=(self.app.font_ui, 11, "bold"),
                fg=p["hud_text"], bg=p["panel"],
                anchor="w",
            ).grid(row=i, column=1, padx=(0, 0), pady=3, sticky="w")

        # ── Divider ───────────────────────────────────────────────────
        tk.Frame(content, height=2, bg=p["bg"]).pack(fill="x", pady=10)

        # ── Buttons: Play Again | Main Menu | Exit ────────────────────
        btn_frame = tk.Frame(content, bg=p["panel"])
        btn_frame.pack(pady=(0, 4))

        def play_again():
            dialog.destroy()
            self._restart()

        def go_menu():
            dialog.destroy()
            self.app.show_menu()

        def exit_game():
            dialog.destroy()
            self.app._on_close()

        for label, cmd, accent in [
            ("🔄  Play Again", play_again, "#2E7D32"),
            ("🏠  Main Menu", go_menu, p["btn_bg"]),
            ("❌  Exit",       exit_game, "#C62828"),
        ]:
            b = tk.Button(
                btn_frame, text=label,
                font=(self.app.font_ui, 10, "bold"),
                fg=p["btn_text"],
                bg=accent,
                activebackground=p["btn_hover"],
                relief="flat", bd=0,
                padx=14, pady=8,
                cursor="hand2",
                command=cmd,
            )
            b.pack(side="left", padx=6)
            self._add_hover(b, p["btn_hover"], accent)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _restart(self):
        """Restart with the same difficulty and player name."""
        self.app.sound.play("button")
        self.app.show_game(self.difficulty)

    def _toggle_sound(self):
        muted = self.app.sound.toggle_mute()
        self._sound_var.set("🔇" if muted else "🔊")


# ═══════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    MinesweeperApp()