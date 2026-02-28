from flask import Flask, jsonify, render_template
import try_traffic_simu
import green_logic
import cv2
import time
import os
import threading
import numpy as np

# ===============================
# 🔁 CHANGE THIS TO SWITCH MODE
# ===============================
MODE = "SIMULATION"   # or "HARDWARE"
# MODE = "HARDWARE" 

if MODE == "HARDWARE":
    import hardware_light

app = Flask(__name__)

video_paths = [
    "nice - traffic signal.mp4",
    "partially ok.mp4",
    "nice - traffic signal.mp4",
    "partially ok.mp4"
]

# Separate capture for display & detection
caps_display = [cv2.VideoCapture(v) for v in video_paths]
caps_detect = [cv2.VideoCapture(v) for v in video_paths]

current_cam = 0

# ===============================
# 🎥 Collage Thread (Simulation Only)
# ===============================
def video_collage_loop():
    while True:
        frames = []

        for cap in caps_display:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            frames.append(frame)

        resized = [cv2.resize(f, (400, 300)) for f in frames]
        top = np.hstack((resized[0], resized[1]))
        bottom = np.hstack((resized[2], resized[3]))
        collage = np.vstack((top, bottom))

        cv2.imshow("Traffic Monitor (2x2)", collage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# ===============================
# 🌐 Web Route (Simulation Mode)
# ===============================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/green-time", methods=["POST"])
def green_time_api():
    global current_cam

    ret, frame = caps_detect[current_cam].read()
    if not ret:
        caps_detect[current_cam].set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = caps_detect[current_cam].read()

    detected_frame, vehicle_data = try_traffic_simu.yoloo(frame)
    green_time = green_logic.green_time(vehicle_data)

    # Save detected image
    folder = f"cam{current_cam+1}"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/detect_{int(time.time())}.jpg"
    cv2.imwrite(filename, detected_frame)

    # ===============================
    # 🚦 HARDWARE MODE EXECUTION
    # ===============================
    if MODE == "HARDWARE":
        hardware_light.run_hardware(current_cam, green_time)

    response = {
        "number": green_time,
        "vehicle-count": vehicle_data,
        "junction": current_cam
    }

    current_cam = (current_cam + 1) % 4

    return jsonify(response)


# ===============================
# ▶ MAIN START
# ===============================
if __name__ == "__main__":

    if MODE == "SIMULATION":
        threading.Thread(target=video_collage_loop, daemon=True).start()
        app.run(debug=True, use_reloader=False)

    else:
        print("Running in HARDWARE mode...")
        while True:
            green_time_api()   # continuously run hardware logic