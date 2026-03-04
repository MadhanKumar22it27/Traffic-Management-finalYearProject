from flask import Flask, jsonify, render_template
import try_traffic_simu
import green_logic
import cv2
import time
import os
import threading
import numpy as np

# =================================
# MODE SWITCH
# =================================
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

# Only ONE set of VideoCapture objects
caps = [cv2.VideoCapture(v) for v in video_paths]

# Shared frame buffer
latest_frames = [None, None, None, None]

current_cam = 0


# =================================
# VIDEO THREAD
# =================================
def video_collage_loop():
    global latest_frames

    while True:

        frames = []

        for i, cap in enumerate(caps):

            ret, frame = cap.read()

            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            latest_frames[i] = frame
            frames.append(frame)

        resized = [cv2.resize(f, (400, 300)) for f in frames]

        top = np.hstack((resized[0], resized[1]))
        bottom = np.hstack((resized[2], resized[3]))
        collage = np.vstack((top, bottom))

        cv2.imshow("Traffic Monitor (2x2)", collage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)


# =================================
# CORE DETECTION FUNCTION
# =================================
def process_junction():

    global current_cam

    frame = latest_frames[current_cam]

    if frame is None:
        return current_cam, 5, {}

    detected_frame, vehicle_data = try_traffic_simu.yoloo(frame)

    green_time = green_logic.green_time(vehicle_data)

    # Save detected image
    folder = f"cam{current_cam+1}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/detect_{int(time.time())}.jpg"
    cv2.imwrite(filename, detected_frame)

    junction = current_cam

    current_cam = (current_cam + 1) % 4

    return junction, green_time, vehicle_data


# =================================
# WEB ROUTES
# =================================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/green-time", methods=["POST"])
def green_time_api():

    junction, green_time, vehicle_data = process_junction()

    if MODE == "HARDWARE":
        hardware_light.run_hardware(junction, green_time)

    return jsonify({
        "number": green_time,
        "vehicle-count": vehicle_data,
        "junction": junction
    })


# =================================
# MAIN START
# =================================
if __name__ == "__main__":

    threading.Thread(target=video_collage_loop, daemon=True).start()

    if MODE == "SIMULATION":

        app.run(debug=True, use_reloader=False)

    else:

        print("Running in HARDWARE mode...")

        while True:

            junction, green_time, vehicle_data = process_junction()

            hardware_light.run_hardware(junction, green_time)