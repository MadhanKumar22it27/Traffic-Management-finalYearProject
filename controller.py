import threading
import time
import cv2
import numpy as np
import try_traffic_simu
import green_logic

video_paths = [
    "nice - traffic signal.mp4",
    "partially ok.mp4",
    "nice - traffic signal.mp4",
    "partially ok.mp4"
]

caps = [cv2.VideoCapture(v) for v in video_paths]

current_state = {
    "active_junction": 0,
    "signals": ["RED", "RED", "RED", "RED"],
    "countdown": 0
}

# ---------------- VIDEO THREAD ----------------
def video_loop():
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


# ---------------- TRAFFIC LOGIC THREAD ----------------
def traffic_loop():
    global current_state
    current_cam = 0

    while True:

        # Yellow phase
        current_state["signals"] = ["RED"] * 4
        current_state["signals"][current_cam] = "YELLOW"
        time.sleep(3)

        # Capture frame for detection
        ret, frame = caps[current_cam].read()
        if not ret:
            caps[current_cam].set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = caps[current_cam].read()

        _, vehicle_data = try_traffic_simu.yoloo(frame)
        green_time = green_logic.green_time(vehicle_data)

        # Green phase
        current_state["signals"] = ["RED"] * 4
        current_state["signals"][current_cam] = "GREEN"

        for sec in range(green_time, -1, -1):
            current_state["countdown"] = sec
            current_state["active_junction"] = current_cam
            time.sleep(1)

        current_cam = (current_cam + 1) % 4


def start_controller():
    video_thread = threading.Thread(target=video_loop)
    traffic_thread = threading.Thread(target=traffic_loop)

    video_thread.daemon = True
    traffic_thread.daemon = True

    video_thread.start()
    traffic_thread.start()