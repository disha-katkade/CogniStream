import tkinter as tk
from threading import Thread, Event
import time
import pyautogui
import cv2
import numpy as np
import pyttsx3  # Added for Voice
from google import genai
from google.genai import types

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyCos0vJ7RvWPRZJvAF_" # Ensure your key is here
client = genai.Client(api_key=API_KEY, http_options=types.HttpOptions(api_version='v1alpha'))

class CogniStreamApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CogniStream")
        self.root.geometry("350x300+1150+50") 
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#121212")

        # --- NEW: VOICE & MEMORY SETUP ---
        try:
            self.voice_engine = pyttsx3.init()
        except:
            self.voice_engine = None
        
        # Start a Chat Session for Contextual Memory
        self.chat_session = client.chats.create(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level="HIGH")
            )
        )

        self.stop_event = Event()
        self._offsetx = 0
        self._offsety = 0

        # 1. HEADER (Top)
        self.header = tk.Label(self.root, text="⠿ COGNISTREAM LIVE", 
                               fg="#00ffcc", bg="#1c1c1c", font=("Consolas", 10, "bold"), cursor="fleur")
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.bind("<Button-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.do_move)

        # 2. BUTTON FRAME (Bottom)
        self.btn_frame = tk.Frame(self.root, bg="#121212")
        self.btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.toggle_btn = tk.Button(self.btn_frame, text="STOP AI", command=self.toggle_ai, 
                                    bg="#ff9900", fg="black", font=("Arial", 9, "bold"), 
                                    bd=0, height=2)
        self.toggle_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.exit_btn = tk.Button(self.btn_frame, text="EXIT", command=self.root.destroy, 
                                  bg="#ff4444", fg="white", font=("Arial", 9, "bold"), 
                                  bd=0, height=2)
        self.exit_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        # 3. ADVICE TEXT AREA (Middle)
        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg="#1e1e1e", fg="#e0e0e0", 
                                 font=("Segoe UI", 10), bd=0, padx=15, pady=15)
        self.text_area.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        
        self.update_ui("AI Engine: Ready. High Reasoning Active...")

        self.start_ai_thread()

    # --- NEW: VISUAL PULSE ---
    def set_pulse(self, active):
        """Changes header color to Blue when thinking, back to Gray when idle."""
        color = "#0055ff" if active else "#1c1c1c"
        self.header.config(bg=color)

    def toggle_ai(self):
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.toggle_btn.config(text="START AI", bg="#00ffcc")
            self.update_ui("AI Engine: PAUSED. Not watching.")
        else:
            self.stop_event.clear()
            self.toggle_btn.config(text="STOP AI", bg="#ff9900")
            self.update_ui("AI Engine: RESUMED...")
            self.start_ai_thread()

    def start_ai_thread(self):
        self.ai_thread = Thread(target=self.vision_loop, daemon=True)
        self.ai_thread.start()

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self._offsetx
        y = self.root.winfo_y() + event.y - self._offsety
        self.root.geometry(f"+{x}+{y}")

    def update_ui(self, message):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, message)

    def vision_loop(self):
        while not self.stop_event.is_set():
            try:
                # 1. Capture & Privacy Blur
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                h, w, _ = frame.shape
                frame[int(h*0.9):h, 0:w] = cv2.GaussianBlur(frame[int(h*0.9):h, 0:w], (51, 51), 0)
                cv2.imwrite("vision_temp.jpg", frame)

                # 2. Pulse Header BLUE (Thinking started)
                self.root.after(0, lambda: self.set_pulse(True))

                with open("vision_temp.jpg", "rb") as f:
                    img_bytes = f.read()

                # --- FIXED LINE BELOW ---
                # In chat.send_message, we pass the parts directly without the 'contents=' keyword
                response = self.chat_session.send_message(
                    message=[
                        types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                        "Observe this screen. Give one helpful tip or identify one error. build on your previous advice if applicable. Max 20 words."
                    ]
                )
                
                # 3. Pulse Header BACK (Thinking finished)
                self.root.after(0, lambda: self.set_pulse(False))
                
                if not self.stop_event.is_set():
                    advice = response.text
                    self.update_ui(advice)
                    
                    # VOICE OUTPUT
                    try:
                        if self.voice_engine:
                            self.voice_engine.say(advice)
                            self.voice_engine.runAndWait()
                    except:
                        pass # Ignore voice errors to keep the UI alive
                
            except Exception as e:
                if "429" in str(e):
                    # Tell the user exactly when to retry
                    self.update_ui("QUOTA EXHAUSTED: Please wait 30 seconds before next scan.")
                    self.root.after(0, lambda: self.set_pulse(False))
                    time.sleep(30) # Force a wait
                else:
                    self.update_ui(f"Status: AI is recalibrating...")
            
            # 30 second delay (Check every 0.1s so STOP button works instantly)
            for _ in range(300):
                if self.stop_event.is_set(): break
                time.sleep(0.1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CogniStreamApp()

    app.run()














