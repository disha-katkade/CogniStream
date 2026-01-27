import tkinter as tk
from threading import Thread
import time

class CogniHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CogniStream HUD")
        
        # 1. Window Settings: Small, Top-Right, Always on Top
        self.root.geometry("350x200+1150+50") 
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True) # Removes borders for a "HUD" look
        self.root.attributes("-alpha", 0.85) # Semi-transparent
        self.root.configure(bg="#1e1e1e") # Dark theme

        # 2. UI Elements
        self.label_title = tk.Label(self.root, text="COGNISTREAM ADVICE", fg="#00ffcc", bg="#1e1e1e", font=("Arial", 10, "bold"))
        self.label_title.pack(pady=5)

        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg="#2d2d2d", fg="white", font=("Arial", 10), bd=0, padx=10, pady=10)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
        # Initial message
        self.update_advice("Analyzing your screen... Keep working!")

        # Exit button (small 'x' in corner)
        self.exit_btn = tk.Button(self.root, text="X", command=self.root.destroy, bg="#1e1e1e", fg="gray", bd=0)
        self.exit_btn.place(x=330, y=0)

    def update_advice(self, text):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)

    def run(self):
        self.root.mainloop()

# To use this with your vision script, we will run the vision loop in a separate "Thread"