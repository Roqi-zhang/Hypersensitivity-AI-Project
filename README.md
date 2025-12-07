# Inner Harbor 🌊  
### An Empathetic AI Companion for Highly Sensitive People (HSP)

> “Friendly as a friend, precise as a professional – an AI that listens, responds, and supports.”

---

## 0. Project Snapshot

- **Project Type**: AI fine-tuning · Affective computing · IoT / Arduino · Future product concept  
- **Timeline**: 2025.05 – 2025.08  
- **Author**: Shihan Zhang  
- **Target Users**: Highly Sensitive People (HSPs) who experience stronger emotional fluctuations and stress in daily life.

This repository documents the **full technical pipeline** of _Inner Harbor_:

1. **Physiological sensing** via Arduino + multiple biosensors  
2. **Real-time emotion detection** based on multi-parameter rules  
3. **Fine-tuned empathetic dialogue model** deployed on Hugging Face Spaces  
4. **Python bridge script** that monitors the body, detects anomalies, and automatically opens the AI companion when needed

The goal is to show not only a demo, but the **complete thinking process** behind the system — from research and concept to engineering implementation.

---

## 1. Concept & Background

Highly Sensitive People (HSPs) are more responsive to emotions, sensations, and social interactions. They are empathetic and observant, but also more prone to anxiety, overwhelm, and fatigue. Many struggle with emotional self-regulation in fast-paced environments.

**Inner Harbor** is my design and engineering response to this group:

- It continuously **monitors physiological signals** (heart rate, HRV, temperature, breath, GSR, blood oxygen, blood pressure, circulation, RR intervals).
- When repeated anomalies are detected, it automatically **launches a fine-tuned AI companion**.
- The AI engages in **emotionally supportive, human-like dialogue**, tailored specifically to the experiences of HSPs.
- In the long term, the concept extends into a future “**Emotion Cloud**” – a soft, responsive companion that surrounds the user in everyday scenes and offers real-time emotional support.

---

## 2. System Overview

The system consists of three main layers:

### **1. Sensing Layer (Hardware + Arduino)**  
- Arduino UNO  
- Integrated physiological sensor module  
- GSR (Galvanic Skin Response) sensor  
- The Arduino fuses data and outputs **JSON** packets via serial

### **2. Processing Layer (Python)**  
- Receives and parses JSON from serial  
- Applies **rule-based emotion detection**  
- Monitors consecutive anomalies  
- Calls Hugging Face API to check whether the AI Space is running  
- If running, automatically opens the emotional-support interface

### **3. Interaction Layer (Hugging Face Space)**  
- Fine-tuned LLM (DeepSeek-R1-Distill-Llama-8B with LoRA)  
- Warm, empathetic, context-aware conversation for emotional grounding  
- Multi-turn dialogue UX optimized for HSP use cases

## 3. Repository Structure

```text
InnerHarbor-HSP-Companion/
├── README.md                # You are reading this file
├── requirements.txt         # Python dependencies
├── sensors/
│   ├── arduino/
│   │   └── HRV_heart_GSR_english_copy_20251118184200.ino
├── webapp/
│   ├── app.py               # Hugging Face Space interface
├── fine-tuned/
│   ├── fine-tuned process.docx    # Fine-tuning steps and code
├── dataset/
│   ├── README.md            # Dataset card & ethics
│   └── samples/             # Sample data
└── docs/
    ├── architecture.png     # System overview diagram
    ├── hardware_setup.jpg   # Sensor + Arduino photo
    └── ui_screenshot.png    # Space interface screenshot
    └── ui_screenshot1.png    # Space interface screenshot
```
  
## 4. Core Python Script Explanation

Main objective:
Monitor physiological parameters → detect anomalies → automatically trigger the AI support interface.

### 4.1 Key Configurations
```

SPACE_ID   = "christinashihan/Your_instantAIfriend"
SPACE_URL  = "https://christinashihan-your-instantaifriend.hf.space"

# IMPORTANT: for safety, do NOT hard-code your token in public repos
HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")

SERIAL_PORT = "COM3"
BAUD_RATE   = 9600
```
🔐 Security Note
In your local environment, create a .env file (not committed to Git) and set:
```
HF_TOKEN=your_real_token_here
```

Then load it in Python via os.getenv("HF_TOKEN") or a library like python-dotenv.

### 4.2 Emotion Detection

Emotion thresholds are defined in a dictionary:
```
EMOTION_THRESHOLDS = {
    "abnormal": {...},
    "anxiety":  {...},
    "anger":    {...},
    "sadness":  {...}
}
```

If 3 indicators match the threshold → emotion detected.

If 3 consecutive detections occur → considered a stable anomaly.

### 4.3 Hugging Face Space Launching

The script calls:
```
https://huggingface.co/api/spaces/<SPACE_ID>
```

Checks runtime.stage:

RUNNING → open Space

BUILDING / SLEEPING → wait (The continuous running time of space is 5 minutes. If space is in the sleeping state, just wake it up)

ERROR → notify user

This prevents 404 issues.

## 5. Arduino Logic Overview

On the Arduino side:

Set baseline for GSR (averaging 500 samples)

Read 24-byte packets from the integrated sensor

Verify header (0xFF) and tail (0xF1)

Extract values:

Heart rate

RR interval

HRV_SDNN

HRV_RMSSD

Body temperature

Breath rate

Blood oxygen

Blood pressure

Circulation

Output JSON once per second

Example output:
```
{
  "HeartRate": 82,
  "BodyTemp": 36.8,
  "GSR": 512,
  "BloodOxygen": 97,
  "BreathRate": 12,
  "BP_High": 120,
  "BP_Low": 80,
  "HRV_SDNN": 35,
  "HRV_RMSSD": 28,
  "RRInterval": 701,
  "Circulation": 10,
  "EmotionDetected": false/detected
}
```
## 6. Model Fine-Tuning & Dataset
### 6.1 Dataset Construction

The fine-tuning dataset includes:

Counseling-style conversations

Emotionally supportive dialogues

HSP-relevant emotional scenarios

Emoji-enhanced empathetic responses

Format:
```
{
  "instruction": "...",
  "input": "...",
  "output": "..."
}
```
### 6.2 Fine-Tuning Pipeline

Base model: DeepSeek-R1-Distill-Llama-8B

Method: LoRA + SFT

Training environment: Google Colab

Deployment: Hugging Face Space

Outcome:
The model responds more warmly, deeply, and contextually — aligned with HSP emotional needs.

## 7. Installation & Usage
### 7.1 Install Dependencies
```
pip install -r requirements.txt
```
### 7.2 Configure Your Environment

Create a .env file:
```
HF_TOKEN=your_hf_token
SPACE_ID=christinashihan/Your_instantAIfriend
SPACE_URL=https://christinashihan-your-instantaifriend.hf.space
SERIAL_PORT=COM3
BAUD_RATE=9600
```
### 7.3 Upload Arduino Sketch

In Arduino IDE:

Open sensors/arduino/inner_harbor.ino

Select correct board + port

Upload

### 7.4 Run the Monitoring Script
```
cd sensors/python
python monitor_and_launch.py
```

The Space will auto-launch when anomalies are detected.

## 8. Ethical Notes

This project is a research & design exploration, not a clinical tool.

Does not diagnose medical conditions

Data is collected with informed consent

AI responses are for emotional support, not therapy

## 9. Future Vision: Emotion Cloud

Inner Harbor evolves into a soft, ambient “Emotion Cloud” that:

Appears in everyday stressful moments

Changes color based on emotional readings

Offers grounding prompts

Provides ambient emotional presence

This repository captures the engineering prototype, while the design concept continues in the portfolio.

## 10. Contact
Shihan Zhang
📍 Creative designer & Technologist & AI Researcher
🔗 Hugging Face: https://huggingface.co/christinashihan
📧 Email: shihanzhang063@gmail.com
