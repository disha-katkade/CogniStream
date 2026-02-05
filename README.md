# CogniStream ⠿ | Gemini 3 AI Coding Partner

**Project for the Gemini 3 Global Hackathon**

CogniStream is a real-time, multimodal HUD (Heads-Up Display) that acts as a proactive coding partner. Using Gemini 3's vision capabilities, it monitors your screen, detects errors, and provides voice-enabled suggestions without requiring manual code input.

---

## 🚀 Gemini 3 Integration
This application leverages the **Gemini 3 Flash** multimodal model to provide low-latency visual reasoning.

* **Visual Reasoning:** Uses Gemini 3 to analyze real-time screen captures of IDEs and UI designs.
* **Contextual Intelligence:** Employs the `thinking_level="HIGH"` configuration for deep-dive logic analysis.
* **Multimodal Feedback:** Translates visual data into concise text tips, delivered via synchronized voice output.

---

## ✨ Features
- **Proactive Debugging:** Automatically identifies logic flaws and syntax errors.
- **Design Critique:** Analyzes UI/UX layouts, alignment, and color contrast.
- **Voice HUD:** Hands-free partner feedback using Text-to-Speech (TTS).
- **Intelligent Activity Sensing:** Minimizes API calls by only scanning when screen changes are detected.

---

## 🛠️ Tech Stack
- **AI:** Gemini 3 API (Google GenAI SDK)
- **Vision:** OpenCV, PyAutoGUI
- **UI/Audio:** Tkinter, pyttsx3
- **Language:** Python 3.x

---

## 📦 Installation & Setup

1. **Clone the Repo:**
   
   ```bash
   git clone [https://github.com/disha-katkade/CogniStream.git](https://github.com/disha-katkade/CogniStream.git)
   cd CogniStream
   ```
1. **Clone the Repo:**
   
   ```bash
   git clone [https://github.com/disha-katkade/CogniStream.git](https://github.com/disha-katkade/CogniStream.git)
   cd CogniStream
   ```
2. **Install Dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```
3. **API Configuration:**
   Create a keys.txt file in the root directory and paste your API Key:
   
   ```bash
   YOUR_GEMINI_API_KEY
   ```
4. **Run Application:**
   
   ```bash
   python CogniStream_app.py
   ```
## 📖 How to Use

1. **Launch the HUD:** Run `python CogniStream_app.py`. The interface will appear as a semi-transparent overlay on the top-right of your screen.
2. **Reposition:** Click and drag the **⠿ COGNISTREAM** header to move the HUD anywhere on your desktop. It is set to "Always on Top" so it stays visible over your IDE.
3. **Select Mode:**
   - **DEBUG Mode (Default):** The AI scans for code errors, logic flaws, and syntax bugs.
   - **DESIGN Mode:** Click the "DESIGN" label to switch the AI's focus to UI layouts, color palettes, and UX improvements.
4. **Monitor Activity:** - The **Status Dot** will blink when the AI is "Thinking" (sending a screen capture to Gemini 3).
   - Scanning occurs automatically when movement is detected on your screen.
5. **Voice Interaction:** Ensure your system volume is up. The AI will read its suggestions out loud so you don't have to stop typing.
6. **Pause/Resume:** Click the **STOP AI** button to stop the vision loop for privacy or performance; click **START AI** to resume.
7. **Exit:** Click the **EXIT** button to safely shut down the threads and close the application.
