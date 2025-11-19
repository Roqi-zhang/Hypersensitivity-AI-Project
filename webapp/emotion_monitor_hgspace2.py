import serial
import time
import webbrowser
import requests
import json

# === Hugging Face related configurations ===
SPACE_ID = "christinashihan/Your_instantAIfriend"
SPACE_URL = "https://christinashihan-your-instantaifriend.hf.space"
HUGGINGFACE_TOKEN = "your_real_token_here"

# === Emotion detection parameters (based on resting heart rate of 60) ===
EMOTION_THRESHOLDS = {
    "abnormal": {
        "hr_min": 60,
        "hr_max": 105,
        "gsr_max": 5,
        "o2_max": 90,
        "bp_sys_max": 140,
        "bp_dia_max": 90,
        "sdnn_min": 45,
        "circ_min": 10,
    },
    "anxiety": {
        "HeartRate_min": 85,
        "BodyTemp_min": 36.8,
        "GSR_min": 600,
        "Fatigue_min": 60,
        "BreathRate_max": 10,
        "HRV_SDNN_max": 30,
        "HRV_RMSSD_max": 25
    },
    "anger": {
        "HeartRate_min": 90,
        "BodyTemp_min": 37.0,
        "GSR_min": 700,
        "BP_High_min": 135,
        "BreathRate_min": 18,
        "Fatigue_min": 50
    },
    "sadness": {
        "HeartRate_max": 65,
        "BodyTemp_max": 36.5,
        "GSR_max": 400,
        "Fatigue_max": 70,
        "BloodOxygen_min": 94,
        "HRV_SDNN_min": 10,
        "HRV_RMSSD_min": 10
    }
}

# === Serial port configuration ===
SERIAL_PORT = "COM3"
BAUD_RATE = 9600

# === Trigger emotion detection ===
def detect_emotion(data):
    for emotion, rules in EMOTION_THRESHOLDS.items():
        count = 0
        for key, threshold in rules.items():
            try:
                if "_min" in key:
                    param = key.replace("_min", "")
                    if data.get(param, 0) >= threshold:
                        count += 1
                elif "_max" in key:
                    param = key.replace("_max", "")
                    if data.get(param, 0) <= threshold:
                        count += 1
            except Exception as e:
                print(f"⚠️ Error fields during detection {key}: {e}")
        if count >= 3:
            print(f"✅ {emotion.upper()} Anomaly detected：{count} Indicator meets the anomaly threshold")
            return emotion
    return None

# === Check whether the Hugging Face Space is ready ===
def wait_for_space_ready():
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    api_url = f"https://huggingface.co/api/spaces/{SPACE_ID}"

    print("🔄 Checking Space status...")
    for _ in range(30):
        try:
            r = requests.get(api_url, headers=headers)
            status = r.json().get("runtime", {}).get("stage", "unknown")
            print(f"🚦 Current Space status：{status}")
            if status.lower() == "running":
                return True
            time.sleep(5)
        except Exception as e:
            print("❌ Status check failed:", e)
            time.sleep(5)
    return False

# === Main program entry point ===
def main():
    print("📡 Monitoring sensor data...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)

    abnormal_count = 0  # Record anomaly count

    try:
        while True:
            line = ser.readline().decode().strip()
            if line:
                try:
                    data = json.loads(line)

                    hr = int(data.get("HeartRate", 0))
                    temp = float(data.get("BodyTemp", 0.0))
                    gsr = int(data.get("GSR", 0))
                    bo = int(data.get("BloodOxygen", 0))
                    fatigue = int(data.get("Fatigue", 0))
                    breath = int(data.get("BreathRate", 0))
                    bp_high = int(data.get("BP_High", 0))
                    bp_low = int(data.get("BP_Low", 0))
                    sdnn = int(data.get("HRV_SDNN", 0))
                    rmssd = int(data.get("HRV_RMSSD", 0))
                    rr = int(data.get("RRInterval", 0))
                    circ = int(data.get("Circulation", 0))
                    detected = data.get("EmotionDetected", False)

                    print(
                        f"❤️ HR: {hr}, 🌡 Temp: {temp}, ⚡️ GSR: {gsr}, 🩸 O2: {bo}, "
                        f"🧠 Fatigue: {fatigue}, 🫁 BR: {breath}, 🔺BP: {bp_high}/{bp_low}, "
                        f"RR: {rr}, SDNN: {sdnn}, RMSSD: {rmssd}, 💧 Circulation: {circ}, 🤖 AutoEmotion: {detected}"
                    )

                    emotion = detect_emotion(data)
                    if emotion:
                        abnormal_count += 1
                        print(f"⚠️ The {abnormal_count} motional anomaly detected (count)：{emotion.upper()}")
                    else:
                        abnormal_count = 0  # Reset counter if one normal reading occurs

                    if abnormal_count >= 3:
                        print(f"🚨 consecutive {abnormal_count} detected, launching Hugging Face Space...")
                        if wait_for_space_ready():
                            webbrowser.open(SPACE_URL)
                        else:
                            print("🚫 Space launch failed, please check network or token configuration")
                        break  # Exit loop after trigger

                except json.JSONDecodeError as e:
                    print("❌ JSON parsing failed:", e)
                except Exception as e:
                    print("❌ Data processing failed:", e)
    except KeyboardInterrupt:
        print("⛔️ Manual monitoring termination")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
