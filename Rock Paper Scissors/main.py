import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import random
import os
import db_manager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images")

class RockPaperScissorsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors Ultra")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.user_data = None # (firstname, gender)
        self.username = ""
        
        # Load Images
        self.load_assets()
        
        # Container for screens
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.show_frame("StartScreen")

    def load_assets(self):
        try:
            # Hands for buttons
            self.rHandPhoto = PhotoImage(file=os.path.join(IMAGE_DIR, "rHand.png"))
            self.pHandPhoto = PhotoImage(file=os.path.join(IMAGE_DIR, "pHand.png"))
            self.sHandPhoto = PhotoImage(file=os.path.join(IMAGE_DIR, "sHand.png"))
            
            # Results images
            self.rockImage = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "Rockimg.jpg")).resize((200, 200)))
            self.paperImage = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "Paperimg.jpg")).resize((200, 200)))
            self.scissorImage = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "Scissorsimg.jpg")).resize((200, 200)))
            
            self.winImage = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "YouWin.jpg")).resize((200, 200)))
            self.loseImage = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "YouLose.jpg")).resize((200, 200)))
            self.tieImage = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "YouTie.jpg")).resize((200, 200)))
            
            self.confettiImg = PhotoImage(file=os.path.join(IMAGE_DIR, "confeti.gif"))
            self.maleImg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "Male.jpg")).resize((150, 150)))
            self.femaleImg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGE_DIR, "Female.jpg")).resize((150, 150)))
            self.compImg = PhotoImage(file=os.path.join(IMAGE_DIR, "computer.png"))
        except Exception as e:
            print(f"Error loading images: {e}")
            messagebox.showwarning("Warning", f"Some images could not be loaded. Please check the 'Images' folder.\nError: {e}")

    def show_frame(self, page_name, **kwargs):
        """Destroys previous frame and creates a new one to ensure clean state."""
        if page_name in self.frames:
            self.frames[page_name].destroy()
            
        if page_name == "StartScreen":
            frame = StartScreen(parent=self.container, controller=self)
        elif page_name == "WelcomeScreen":
            frame = WelcomeScreen(parent=self.container, controller=self)
        elif page_name == "GameScreen":
            frame = GameScreen(parent=self.container, controller=self)
        elif page_name == "LeaderboardScreen":
            frame = LeaderboardScreen(parent=self.container, controller=self)
        else:
            return

        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")
        
        label = tk.Label(self, text="Rock Paper Scissors", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        label.pack(pady=20)
        
        self.toggle_frame = tk.Frame(self, bg="#f0f0f0")
        self.toggle_frame.pack(pady=10)
        
        self.login_btn = tk.Button(self.toggle_frame, text="Login", width=15, command=self.show_login, bg="#0074ff", fg="white")
        self.login_btn.grid(row=0, column=0, padx=5)
        
        self.signup_btn = tk.Button(self.toggle_frame, text="Sign Up", width=15, command=self.show_signup, bg="#19a8f2", fg="white")
        self.signup_btn.grid(row=0, column=1, padx=5)
        
        self.form_container = tk.Frame(self, bg="#f0f0f0", borderwidth=2, relief="groove", padx=20, pady=20)
        self.form_container.pack(pady=20)
        
        self.show_login()

    def show_login(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        self.login_btn.configure(bg="#0074ff")
        self.signup_btn.configure(bg="#19a8f2")
        
        tk.Label(self.form_container, text="Username:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.form_container, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(self.form_container, text="Password:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.form_container, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        tk.Button(self.form_container, text="Log In", bg="green", fg="white", width=20, command=self.handle_login).grid(row=2, column=0, columnspan=2, pady=15)

    def show_signup(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()
            
        self.login_btn.configure(bg="#19a8f2")
        self.signup_btn.configure(bg="#0074ff")
        
        fields = ["Firstname", "Lastname", "Username", "Password"]
        self.signup_entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(self.form_container, text=f"{field}:", bg="#f0f0f0").grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(self.form_container, width=30)
            if field == "Password": entry.configure(show="*")
            entry.grid(row=i, column=1, pady=2)
            self.signup_entries[field] = entry
            
        tk.Label(self.form_container, text="Gender:", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=2)
        self.gender_var = tk.StringVar(value="Male")
        tk.Radiobutton(self.form_container, text="Male", variable=self.gender_var, value="Male", bg="#f0f0f0").grid(row=4, column=1, sticky="w")
        tk.Radiobutton(self.form_container, text="Female", variable=self.gender_var, value="Female", bg="#f0f0f0").grid(row=5, column=1, sticky="w")
        
        tk.Button(self.form_container, text="Sign Up", bg="green", fg="white", width=20, command=self.handle_signup).grid(row=6, column=0, columnspan=2, pady=15)

    def handle_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        data = db_manager.check_user(user, pwd)
        if data:
            self.controller.user_data = data # (firstname, gender)
            self.controller.username = user
            self.controller.show_frame("WelcomeScreen")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def handle_signup(self):
        d = {k: v.get() for k, v in self.signup_entries.items()}
        gender = self.gender_var.get()
        if all(d.values()):
            if db_manager.register_user(d["Firstname"], d["Lastname"], d["Username"], d["Password"], gender):
                messagebox.showinfo("Success", "Account created! Please log in.")
                self.show_login()
            else:
                messagebox.showerror("Error", "Registration failed.")
        else:
            messagebox.showwarning("Warning", "All fields are required.")

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        name = controller.user_data[0]
        gender = controller.user_data[1]
        
        tk.Label(self, text=f"Welcome, {name}!", font=("Helvetica", 24, "bold"), bg="white", pady=30).pack()
        
        img_frame = tk.Frame(self, bg="white")
        img_frame.pack(pady=20)
        
        user_img = controller.maleImg if gender == "Male" else controller.femaleImg
        tk.Label(img_frame, image=user_img, bg="white").grid(row=0, column=0, padx=40)
        tk.Label(img_frame, text="VS", font=("Helvetica", 20, "bold"), bg="white").grid(row=0, column=1)
        tk.Label(img_frame, image=controller.compImg, bg="white").grid(row=0, column=2, padx=40)
        
        tk.Button(self, text="Start Game", font=("Helvetica", 14), bg="green", fg="white", width=20, pady=10, 
                  command=lambda: controller.show_frame("GameScreen")).pack(pady=40)

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#e0e0e0")
        
        self.user_win = 0
        self.comp_win = 0
        self.turns_played = 0
        self.max_turns = 5
        self.click_ready = True
        
        # UI Setup
        self.create_widgets()

    def create_widgets(self):
        # Labels for Choices
        self.label_frame = tk.Frame(self, bg="#e0e0e0")
        self.label_frame.pack(pady=10)
        
        self.user_label = tk.Label(self.label_frame, text="User Choice", bg="#238f02", fg="white", width=25, pady=10)
        self.user_label.grid(row=0, column=0, padx=10)
        
        self.vs_label = tk.Label(self.label_frame, text="VS", font=("bold", 12), bg="#e0e0e0")
        self.vs_label.grid(row=0, column=1)
        
        self.comp_label = tk.Label(self.label_frame, text="Computer Choice", bg="#c20c0c", fg="white", width=25, pady=10)
        self.comp_label.grid(row=0, column=2, padx=10)

        # Buttons/Images Frame
        self.btn_frame = tk.Frame(self, bg="#e0e0e0")
        self.btn_frame.pack(pady=10)
        
        self.rock_btn = tk.Button(self.btn_frame, image=self.controller.rHandPhoto, command=lambda: self.play("rock"))
        self.rock_btn.grid(row=0, column=0, padx=10)
        
        self.paper_btn = tk.Button(self.btn_frame, image=self.controller.pHandPhoto, command=lambda: self.play("paper"))
        self.paper_btn.grid(row=0, column=1, padx=10)
        
        self.scissors_btn = tk.Button(self.btn_frame, image=self.controller.sHandPhoto, command=lambda: self.play("scissors"))
        self.scissors_btn.grid(row=0, column=2, padx=10)

        # Score and Controls
        self.bottom_frame = tk.Frame(self, bg="#e0e0e0")
        self.bottom_frame.pack(pady=20, fill="x")
        
        self.score_label = tk.Label(self.bottom_frame, text=f"SCORE\n\nUSER - 0    |    COMPUTER - 0", 
                                   bg="blue", fg="white", font=("Times", 16), pady=20)
        self.score_label.pack(side="left", expand=True, fill="x", padx=20)
        
        self.ctrl_frame = tk.Frame(self.bottom_frame, bg="#e0e0e0")
        self.ctrl_frame.pack(side="right", padx=20)
        
        tk.Button(self.ctrl_frame, text="RESET", bg="green", fg="white", width=15, pady=5, command=self.reset_ui).pack(pady=5)
        tk.Button(self.ctrl_frame, text="LEADERBOARD", bg="black", fg="white", width=15, pady=5, 
                  command=lambda: self.controller.show_frame("LeaderboardScreen")).pack(pady=5)

    def play(self, user_choice):
        if not self.click_ready:
            self.reset_ui()
            return
            
        comp_choice = random.choice(["rock", "paper", "scissors"])
        self.turns_played += 1
        
        # Map choices to images
        img_map = {"rock": self.controller.rockImage, "paper": self.controller.paperImage, "scissors": self.controller.scissorImage}
        
        # Determine Winner
        result = "tie"
        if user_choice == comp_choice:
            result = "tie"
        elif (user_choice == "rock" and comp_choice == "scissors") or \
             (user_choice == "paper" and comp_choice == "rock") or \
             (user_choice == "scissors" and comp_choice == "paper"):
            result = "win"
            self.user_win += 1
        else:
            result = "lose"
            self.comp_win += 1
            
        # Update UI Images
        self.rock_btn.config(image=img_map[user_choice])
        self.paper_btn.config(image=img_map[comp_choice])
        
        if result == "win":
            self.scissors_btn.config(image=self.controller.winImage)
            self.vs_label.config(text="YOU WIN!", fg="green")
        elif result == "lose":
            self.scissors_btn.config(image=self.controller.loseImage)
            self.vs_label.config(text="YOU LOSE!", fg="red")
        else:
            self.scissors_btn.config(image=self.controller.tieImage)
            self.vs_label.config(text="TIE!", fg="orange")
            
        self.score_label.config(text=f"SCORE\n\nUSER - {self.user_win}    |    COMPUTER - {self.comp_win}")
        self.click_ready = False
        
        if self.turns_played >= self.max_turns:
            self.after(1000, self.finish_game)

    def reset_ui(self):
        self.rock_btn.config(image=self.controller.rHandPhoto)
        self.paper_btn.config(image=self.controller.pHandPhoto)
        self.scissors_btn.config(image=self.controller.sHandPhoto)
        self.vs_label.config(text="VS", fg="black")
        self.click_ready = True

    def finish_game(self):
        msg = ""
        is_tie = False
        if self.user_win > self.comp_win:
            msg = "CONGRATULATIONS!\nYou Won the Series!!"
        elif self.user_win < self.comp_win:
            msg = "GAME OVER!\nYou Lost the Series!!"
        else:
            msg = "IT'S A TIE!\nGood Game!"
            is_tie = True
            
        # Update DB
        db_manager.update_leaderboard(self.controller.user_data[0], self.user_win, self.comp_win, is_tie)
        
        # Show Result Dialog
        ResultDialog(self, msg, self.controller)

class ResultDialog(tk.Toplevel):
    def __init__(self, parent, message, controller):
        super().__init__(parent)
        self.title("Game Over")
        self.geometry("300x400")
        self.resizable(False, False)
        self.controller = controller
        
        bg_label = tk.Label(self, image=controller.confettiImg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        content = tk.Frame(self, bg="white", padx=20, pady=20)
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(content, text=message, font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        
        tk.Button(content, text="Play Again", bg="#8953ff", fg="white", width=15, 
                  command=self.play_again).pack(pady=5)
        tk.Button(content, text="Leaderboard", bg="black", fg="white", width=15, 
                  command=self.show_leaderboard).pack(pady=5)
        tk.Button(content, text="Exit", bg="red", fg="white", width=15, 
                  command=controller.quit).pack(pady=5)

    def play_again(self):
        self.destroy()
        self.controller.show_frame("GameScreen")

    def show_leaderboard(self):
        self.destroy()
        self.controller.show_frame("LeaderboardScreen")

class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        tk.Label(self, text="Leaderboard", font=("Times", 24, "bold"), bg="#dd2c00", fg="white", pady=10).pack(fill="x")
        
        self.table_container = tk.Frame(self, bg="white")
        self.table_container.pack(fill="both", expand=True)

        self.table_frame = tk.Frame(self.table_container, bg="white", padx=10, pady=10)
        self.table_frame.pack()
        
        self.headers = ["Name", "Won", "Lost", "Tied", "Played", "Rate"]
        self.header_colors = ["#0069b3", "#a617ff", "#e01717", "#e77c00", "#30b000", "#ff1f60"]
        
        self.load_data()
        
        btn_frame = tk.Frame(self, bg="white", pady=20)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Light Theme", bg="black", fg="white", width=15, command=lambda: self.change_theme("white")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Dark Theme", bg="black", fg="white", width=15, command=lambda: self.change_theme("black")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Back to Game", bg="green", fg="white", width=15, 
                  command=lambda: controller.show_frame("GameScreen")).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Logout", bg="red", fg="white", width=15, 
                  command=lambda: controller.show_frame("StartScreen")).grid(row=0, column=3, padx=5)

    def change_theme(self, color):
        self.configure(bg=color)
        self.table_container.configure(bg=color)
        self.table_frame.configure(bg=color)

    def load_data(self):
        data = db_manager.get_leaderboard_data()
        
        for i, (h, c) in enumerate(zip(self.headers, self.header_colors)):
            tk.Label(self.table_frame, text=h, width=12, bg=c, fg="white", padx=5, pady=5).grid(row=0, column=i, padx=1, pady=1)

        row_colors = ["#3d7eac", "#b846ff", "#e33f3f", "#e38d2a", "#62be40", "#ff5385"]
        
        for r_idx, record in enumerate(data):
            if r_idx > 10: break # Show top 10
            for c_idx, val in enumerate(record):
                tk.Label(self.table_frame, text=val, width=12, bg=row_colors[c_idx], fg="white", padx=5, pady=5).grid(row=r_idx+1, column=c_idx, padx=1, pady=1)

if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()