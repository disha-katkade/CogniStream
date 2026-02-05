# CogniStream ⠿ | Gemini 3 AI Coding Partner

> **Project for the Gemini 3 Global Hackathon**

> CogniStream is a real-time, multimodal HUD (Heads-Up Display) that acts as a proactive coding partner. Using Gemini 3's vision capabilities, it monitors your screen, detects errors, and provides voice-enabled
> suggestions without requiring manual code input.

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

### **AI & Reasoning**
![Gemini](https://img.shields.io/badge/Google_Gemini_3-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

### **Computer Vision & Automation**
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-FFD43B?style=for-the-badge&logo=python&logoColor=3776AB)

### **Frontend & Audio**
![Tkinter](https://img.shields.io/badge/Tkinter_GUI-gray?style=for-the-badge)
![TTS](https://img.shields.io/badge/Pyttsx3_TTS-FF6F61?style=for-the-badge)

### **Version Control & Deployment**
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
---

## 📦 Installation & Setup

1. **Clone the Repo:**
   
   ```bash
   git clone https://github.com/disha-katkade/CogniStream.git
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
### 📖 User Guide

| Feature | Control | Function |
| :--- | :--- | :--- |
| **Launch** | Terminal Command | Run `python CogniStream_app.py` to start the HUD. |
| **Move** | Header Drag | Click and drag the header to reposition the window. |
| **Debug** | `DEBUG` Mode | Focuses AI on logic, bugs, and syntax errors. |
| **Design** | `DESIGN` Mode | Focuses AI on UI/UX, layouts, and aesthetics. |
| **Status** | Blinking Dot | Indicates when Gemini 3 is active and thinking. |
| **Voice** | Auto-Audio | Partner suggestions are read aloud automatically. |
| **Control** | `START` / `STOP` | Toggles the screen scanning loop for privacy. |
| **Close** | `EXIT` | Terminates all threads and closes the app safely. |
