import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

def yoloo(frame):

    height, width, _ = frame.shape

    line_5m_y = int(height * 0.7)
    line_10m_y = int(height * 0.5)
    line_15m_y = int(height * 0.4)

    results = model(frame, conf=0.3)

    vehicle_info = {5: {}, 10: {}, 15: {}}

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label == "motorcycle":
                label = "bike"

            if label not in ["car", "bike", "bus", "truck"]:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_y = (y1 + y2) // 2

            if center_y < line_15m_y:
                continue

            if center_y > line_5m_y:
                meter = 5
            elif center_y > line_10m_y:
                meter = 10
            else:
                meter = 15

            if label not in vehicle_info[meter]:
                vehicle_info[meter][label] = 0

            vehicle_info[meter][label] += 1

            # Draw detection box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, vehicle_info