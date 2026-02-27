import threading
import time
import cv2
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

def traffic_loop():
    global current_state
    current_cam = 0

    while True:

        # Yellow phase
        current_state["signals"] = ["RED"] * 4
        current_state["signals"][current_cam] = "YELLOW"
        time.sleep(3)

        # Capture frame
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
    thread = threading.Thread(target=traffic_loop)
    thread.daemon = True
    thread.start()