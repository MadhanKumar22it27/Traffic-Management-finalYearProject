from flask import Flask, jsonify
import try_traffic_simu
import green_logic
import cv2
import time

app = Flask(__name__)

video_paths = [
    "nice - traffic signal.mp4",
    "partially ok.mp4",
    "nice - traffic signal.mp4",
    "partially ok.mp4"
]

caps = [cv2.VideoCapture(v) for v in video_paths]
current_cam = 0

@app.route("/")
def home():
    return open("templates/index.html").read()

@app.route("/green-time", methods=["POST"])
def green_time_api():
    global current_cam

    ret, frame = caps[current_cam].read()
    if not ret:
        caps[current_cam].set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = caps[current_cam].read()

    detected_frame, vehicle_data = try_traffic_simu.yoloo(frame)
    green_time = green_logic.green_time(vehicle_data)

    # ---------------- SAVE IMAGE ----------------
    import os
    folder = f"cam{current_cam+1}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/detect_{int(time.time())}.jpg"
    cv2.imwrite(filename, detected_frame)

    response = {
        "number": green_time,
        "vehicle-count": vehicle_data,
        "junction": current_cam
    }

    current_cam = (current_cam + 1) % 4

    return jsonify(response)
import threading
import numpy as np

def video_collage_loop():
    while True:
        frames = []

        for cap in caps:
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

if __name__ == "__main__":
    threading.Thread(target=video_collage_loop, daemon=True).start()
    app.run(debug=True, use_reloader=False)