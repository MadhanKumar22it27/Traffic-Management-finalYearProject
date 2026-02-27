import cv2
import numpy as np
import time

def simulate_light(junction, green_time):

    img = np.zeros((300, 300, 3), dtype=np.uint8)

    for sec in range(green_time, -1, -1):

        img[:] = (0, 0, 0)

        # Red circle
        cv2.circle(img, (150, 60), 30, (0, 0, 255), -1)

        # Yellow circle
        cv2.circle(img, (150, 150), 30, (0, 255, 255), -1)

        # Green circle (ON)
        cv2.circle(img, (150, 240), 30, (0, 255, 0), -1)

        cv2.putText(img, f"Junction {junction}",
                    (50, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)

        cv2.putText(img, f"{sec} sec",
                    (100, 290), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255,255,255), 2)

        cv2.imshow("SIMULATION TRAFFIC LIGHT", img)
        cv2.waitKey(1)
        time.sleep(1)