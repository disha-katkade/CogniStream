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
