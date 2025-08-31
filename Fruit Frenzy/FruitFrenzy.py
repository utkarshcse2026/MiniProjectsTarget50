import tkinter as tk
import random
from PIL import Image, ImageTk
import pygame
import sys
import os

# --- Helper Function for PyInstaller ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Game Constants ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 70
PLAYER_SPEED = 35
FRUIT_SIZE = 45
UPDATE_DELAY = 30
MAX_FRUITS = 4
STARTING_LIVES = 3

# --- Asset File Names (using the helper function) ---
INTRO_GIF_FILE = resource_path("intro.gif")
MUSIC_FILE = resource_path("1.mp3")
CATCH_SOUND_FILE = resource_path("1.mp3") # Make sure you have a file named "1.mp3"
HIGHSCORE_FILE = resource_path("highscore.txt")

# --- UI Customization ---
BG_COLOR = "#a2d2ff"
PLAYER_EMOJI = "🧺"
FRUITS_EMOJI = ["🍎", "🍓", "🍊", "🍇", "🍌", "🍒", "🍑"]
HEART_EMOJI = "❤️"
PUNCHLINES = [
    "Looks like you couldn't 'ketchup'!",
    "That was the 'apple' of my eye!",
    "You're 'berry' bad at this!",
    "'Orange' you glad you tried?",
    "That slip-up was 'bananas'!",
]

class FruityFrenzyGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Fruity Frenzy")
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.master.resizable(False, False)

        # --- IMPORTANT: Handle window close event gracefully ---
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        pygame.mixer.init()
        self.load_music()
        self.load_sounds()

        self.high_score = self.load_high_score()
        self.canvas = tk.Canvas(master, bg=BG_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
        self.canvas.pack()

        self.score = 0
        self.lives = STARTING_LIVES
        self.game_running = False
        self.fruits = []
        self.gif_frames = []
        self.gif_frame_index = 0

        self.setup_intro_screen()
        self.setup_game_elements()
        self.setup_game_over_screen()

        self.show_intro_screen()

    def on_close(self):
        """Handles the window closing event to prevent crashes."""
        print("Closing game safely...")
        self.game_running = False  # Stop the game loop
        pygame.quit()  # Cleanly shut down pygame
        self.master.destroy()  # Safely close the Tkinter window

    def setup_intro_screen(self):
        try:
            self.load_gif_frames()
            self.intro_gif_label = tk.Label(self.master, bg=BG_COLOR)
            self.intro_title = self.canvas.create_text(
                WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100,
                text="Fruity Frenzy", font=("Goudy Stout", 50),
                fill="white", state=tk.HIDDEN
            )
            self.start_button = tk.Button(
                self.master, text="Start Game", font=("Helvetica", 25, "bold"),
                command=self.start_game, relief="raised", borderwidth=5,
                bg="#4CAF50", fg="white"
            )
        except (FileNotFoundError, tk.TclError):
            self.intro_gif_label = None
            print(f"Error: '{INTRO_GIF_FILE}' not found or is invalid. The intro screen will be static.")
            self.start_button = tk.Button(self.master, text="Start Game (intro.gif not found)", command=self.start_game)


    def setup_game_elements(self):
        self.player = self.canvas.create_text(0, 0, text=PLAYER_EMOJI, font=("Arial", PLAYER_SIZE), state=tk.HIDDEN)
        for _ in range(MAX_FRUITS):
            fruit_item = self.canvas.create_text(0, 0, text="", font=("Arial", FRUIT_SIZE), state=tk.HIDDEN)
            self.fruits.append({'item': fruit_item, 'speed': 1})
        self.score_label = self.canvas.create_text(15, 15, anchor="nw", text="", font=("Helvetica", 20, "bold"), fill="white", state=tk.HIDDEN)
        self.lives_label = self.canvas.create_text(WINDOW_WIDTH / 2, 28, anchor="center", text="", font=("Helvetica", 22, "bold"), fill="#ff4d4d", state=tk.HIDDEN)
        self.highscore_label = self.canvas.create_text(WINDOW_WIDTH - 15, 15, anchor="ne", text="", font=("Helvetica", 20, "bold"), fill="white", state=tk.HIDDEN)

    def setup_game_over_screen(self):
        self.game_over_text = self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, text="GAME OVER", font=("Helvetica", 50, "bold"), fill="#ff5733", state=tk.HIDDEN)
        self.punchline_text = self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text="", font=("Helvetica", 20, "italic"), fill="black", state=tk.HIDDEN)
        self.restart_button = tk.Button(self.master, text="Restart", font=("Helvetica", 20), command=self.start_game, relief="raised", borderwidth=3, bg="#4CAF50", fg="white")

    def show_intro_screen(self):
        if self.intro_gif_label and self.gif_frames:
            self.intro_gif_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.update_gif(0)
            self.canvas.itemconfig(self.intro_title, state=tk.NORMAL)
        self.start_button.place(relx=0.5, rely=0.5, y=50, anchor="center")
        self.master.bind("<KeyPress>", lambda e: None)
        self.play_music()

    def start_game(self):
        self.start_button.place_forget()
        if self.intro_gif_label: self.intro_gif_label.place_forget()
        self.canvas.itemconfig(self.intro_title, state=tk.HIDDEN)
        self.restart_button.place_forget()
        self.canvas.itemconfig(self.game_over_text, state=tk.HIDDEN)
        self.canvas.itemconfig(self.punchline_text, state=tk.HIDDEN)
        
        self.game_running = True
        self.score = 0
        self.lives = STARTING_LIVES
        self.update_score_label()
        self.update_lives_label()
        self.canvas.itemconfig(self.highscore_label, text=f"High Score: {self.high_score}", state=tk.NORMAL)
        self.canvas.itemconfig(self.score_label, state=tk.NORMAL)
        self.canvas.itemconfig(self.lives_label, state=tk.NORMAL)
        self.canvas.itemconfig(self.player, state=tk.NORMAL)
        self.canvas.coords(self.player, WINDOW_WIDTH / 2, WINDOW_HEIGHT - PLAYER_SIZE)
        
        for fruit in self.fruits:
            self.canvas.itemconfig(fruit['item'], state=tk.NORMAL)
            self.reset_fruit(fruit)

        self.master.bind("<KeyPress>", self.move_player)
        self.update_game()
    
    def load_gif_frames(self):
        gif = Image.open(INTRO_GIF_FILE)
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
            self.gif_frames.append(ImageTk.PhotoImage(frame))

    def update_gif(self, frame_index):
        if self.game_running or not self.gif_frames: return
        frame = self.gif_frames[frame_index]
        self.intro_gif_label.config(image=frame)
        next_frame_index = (frame_index + 1) % len(self.gif_frames)
        self.master.after(50, self.update_gif, next_frame_index)

    def load_music(self):
        try:
            pygame.mixer.music.load(MUSIC_FILE)
        except pygame.error:
            print(f"Error: '{MUSIC_FILE}' not found. Music will not be played.")

    def load_sounds(self):
        try:
            self.catch_sound = pygame.mixer.Sound(CATCH_SOUND_FILE)
        except pygame.error:
            self.catch_sound = None
            print(f"Error: '{CATCH_SOUND_FILE}' not found. Catch sound will not be played.")

    def play_catch_sound(self):
        if self.catch_sound:
            self.catch_sound.play()

    def play_music(self):
        try:
            pygame.mixer.music.play(loops=-1)
        except pygame.error:
            pass

    def update_game(self):
        if not self.game_running: return
        player_bbox = self.canvas.bbox(self.player)
        for fruit in self.fruits:
            self.canvas.move(fruit['item'], 0, fruit['speed'])
            fruit_bbox = self.canvas.bbox(fruit['item'])
            if not fruit_bbox: continue
            if player_bbox and (player_bbox[0] < fruit_bbox[2] and player_bbox[2] > fruit_bbox[0] and player_bbox[1] < fruit_bbox[3] and player_bbox[3] > fruit_bbox[1]):
                self.score += 1
                self.play_catch_sound()
                self.update_score_label()
                self.reset_fruit(fruit)
            elif self.canvas.coords(fruit['item'])[1] > WINDOW_HEIGHT:
                self.lives -= 1
                self.update_lives_label()
                self.reset_fruit(fruit)
                if self.lives <= 0:
                    self.end_game()
                    return
        self.master.after(UPDATE_DELAY, self.update_game)

    def end_game(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.canvas.itemconfig(self.highscore_label, text=f"High Score: {self.high_score}")
        self.canvas.itemconfig(self.game_over_text, state=tk.NORMAL)
        self.canvas.itemconfig(self.punchline_text, text=random.choice(PUNCHLINES), state=tk.NORMAL)
        self.restart_button.place(relx=0.5, rely=0.5, y=60, anchor="center")

    def reset_fruit(self, fruit):
        fruit['speed'] = random.uniform(4.0, 9.0)
        x_start = random.randint(FRUIT_SIZE, WINDOW_WIDTH - FRUIT_SIZE)
        y_start = -random.randint(FRUIT_SIZE, WINDOW_HEIGHT // 2)
        self.canvas.itemconfig(fruit['item'], text=random.choice(FRUITS_EMOJI))
        self.canvas.coords(fruit['item'], x_start, y_start)

    def move_player(self, event):
        if not self.game_running: return
        x, y = self.canvas.coords(self.player)
        if event.keysym == "Left" and x > PLAYER_SIZE / 2: self.canvas.move(self.player, -PLAYER_SPEED, 0)
        elif event.keysym == "Right" and x < WINDOW_WIDTH - PLAYER_SIZE / 2: self.canvas.move(self.player, PLAYER_SPEED, 0)
        elif event.keysym == "Up" and y > WINDOW_HEIGHT / 2: self.canvas.move(self.player, 0, -PLAYER_SPEED)
        elif event.keysym == "Down" and y < WINDOW_HEIGHT - PLAYER_SIZE / 2: self.canvas.move(self.player, 0, PLAYER_SPEED)

    def update_score_label(self): self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
    def update_lives_label(self): self.canvas.itemconfig(self.lives_label, text=HEART_EMOJI * self.lives)
    def load_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "r") as f: return int(f.read())
        except (FileNotFoundError, ValueError): return 0
    def save_high_score(self):
        with open(HIGHSCORE_FILE, "w") as f: f.write(str(self.high_score))


if __name__ == "__main__":
    root = tk.Tk()
    game = FruityFrenzyGame(root)
    root.mainloop()