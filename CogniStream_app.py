<<<<<<< HEAD
import tkinter as tk
from threading import Thread, Event
import time
import pyautogui
import cv2
import numpy as np
import pyttsx3  # Added for voice
from google import genai
from google.genai import types

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyD6nsO7iKdjQh8A_jr7YjhP6eXcO4WXpao" # Your API Key here
client = genai.Client(api_key=API_KEY, http_options=types.HttpOptions(api_version='v1alpha'))

class CogniStreamApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CogniStream")
        self.root.geometry("350x380+1150+50") 
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#0a0a0a")

        self.chat_session = client.chats.create(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level="HIGH")
            )
        )

        self.stop_event = Event()
        self._offsetx = 0
        self._offsety = 0
        self.is_thinking = False
        self.previous_frame = None
        self.current_mode = "DEBUG"

        # 1. HEADER
        self.header_frame = tk.Frame(self.root, bg="#161616", height=40)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        
        self.status_dot = tk.Canvas(self.header_frame, width=20, height=20, bg="#161616", highlightthickness=0)
        self.status_dot.pack(side=tk.LEFT, padx=10)
        self.dot_circle = self.status_dot.create_oval(5, 5, 15, 15, fill="#333333", outline="")

        # Mode Toggles
        self.debug_btn = tk.Label(self.header_frame, text="DEBUG", fg="#00ffcc", bg="#161616", font=("Consolas", 8, "bold"), cursor="hand2")
        self.debug_btn.pack(side=tk.RIGHT, padx=10)
        self.debug_btn.bind("<Button-1>", lambda e: self.set_mode("DEBUG"))

        self.design_btn = tk.Label(self.header_frame, text="DESIGN", fg="#555555", bg="#161616", font=("Consolas", 8, "bold"), cursor="hand2")
        self.design_btn.pack(side=tk.RIGHT, padx=5)
        self.design_btn.bind("<Button-1>", lambda e: self.set_mode("DESIGN"))

        self.header_label = tk.Label(self.header_frame, text="⠿ COGNISTREAM", fg="#ffffff", bg="#161616", font=("Consolas", 10, "bold"))
        self.header_label.pack(side=tk.LEFT)
        self.header_frame.bind("<Button-1>", self.start_move)
        self.header_frame.bind("<B1-Motion>", self.do_move)

        # 2. BUTTONS
        self.btn_frame = tk.Frame(self.root, bg="#0a0a0a", pady=15)
        self.btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.toggle_btn = tk.Button(self.btn_frame, text="STOP AI", command=self.toggle_ai, bg="#ff2a6d", fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0, height=2)
        self.toggle_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        self.exit_btn = tk.Button(self.btn_frame, text="EXIT", command=self.root.destroy, bg="#2d2d2d", fg="#aaaaaa", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, bd=0, height=2)
        self.exit_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)

        # 3. TEXT AREA
        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg="#111111", fg="#e0e0e0", font=("Consolas", 10), bd=0, padx=20, pady=20)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
        self.update_ui("Ready to help, partner! I'm watching the screen.")
        self.start_ai_thread()
        self.animate_dot()

    def set_mode(self, mode):
        self.current_mode = mode
        self.debug_btn.config(fg="#00ffcc" if mode == "DEBUG" else "#555555")
        self.design_btn.config(fg="#ff00ff" if mode == "DESIGN" else "#555555")
        self.update_ui(f"Switched to {mode} mode. Let's get to work.")

    def animate_dot(self):
        if self.is_thinking:
            color = "#00ffcc" if self.current_mode == "DEBUG" else "#ff00ff"
            curr = self.status_dot.itemcget(self.dot_circle, "fill")
            self.status_dot.itemconfig(self.dot_circle, fill=color if curr == "#333333" else "#333333")
        else:
            self.status_dot.itemconfig(self.dot_circle, fill="#333333")
        self.root.after(500, self.animate_dot)

    def toggle_ai(self):
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.toggle_btn.config(text="START AI", bg="#05d9e8", fg="black")
            self.update_ui("Paused. Let me know when you need me.")
        else:
            self.stop_event.clear()
            self.toggle_btn.config(text="STOP AI", bg="#ff2a6d", fg="white")
            self.update_ui("I'm back. Scanning now...")
            self.start_ai_thread()

    # --- UPDATED SPEAKING HELPER (More reliable) ---
    def speak(self, text):
        def _speak_task():
            try:
                # We initialize inside the thread so it doesn't conflict
                speaker = pyttsx3.init()
                speaker.setProperty('rate', 170)
                speaker.say(text)
                speaker.runAndWait()
                speaker.stop() # Clean up after speaking
            except:
                pass
        Thread(target=_speak_task, daemon=True).start()
    # -----------------------------------------------

    def update_ui(self, msg):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"» {msg}")
        # Strip out emojis/non-ASCII characters for the voice engine
        clean_msg = msg.encode('ascii', 'ignore').decode('ascii').strip()
        self.speak(clean_msg) # Trigger the reliable voice helper

    def vision_loop(self):
        while not self.stop_event.is_set():
            try:
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.previous_frame is not None:
                    diff = cv2.absdiff(self.previous_frame, gray)
                    if (np.count_nonzero(cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]) / gray.size) * 100 < 0.1:
                        time.sleep(2)
                        continue
                self.previous_frame = gray

                cv2.imwrite("vision_temp.jpg", frame)
                self.is_thinking = True

                prompt = f"You are a helpful coding partner. Look at the whole screen. I am in {self.current_mode} mode. Give me one helpful suggestion or notice a mistake I'm making. Keep it under 20 words and be friendly."

                with open("vision_temp.jpg", "rb") as f:
                    img_bytes = f.read()
                    response = self.chat_session.send_message(
                        message=[types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"), prompt]
                    )
                
                self.is_thinking = False
                if not self.stop_event.is_set():
                    self.update_ui(response.text)
                
            except Exception as e:
                self.is_thinking = False
                print(f"Error: {e}")
            
            time.sleep(6)

    def start_ai_thread(self):
        Thread(target=self.vision_loop, daemon=True).start()

    def start_move(self, event): self._offsetx, self._offsety = event.x, event.y
    def do_move(self, event):
        x, y = self.root.winfo_x() + event.x - self._offsetx, self.root.winfo_y() + event.y - self._offsety
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    CogniStreamApp().root.mainloop()
=======
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
API_KEY = "----" # Ensure your key is here
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



























>>>>>>> 472404da6e8878ef01698a9e1feca2ad89fcba94
