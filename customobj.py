import cv2

cap = cv2.VideoCapture(0)
cv2.namedWindow("Select Object (Press 's' to Confirm)")

roi = None

def select_roi(event, x, y, flags, param):
    global roi
    if event == cv2.EVENT_LBUTTONDOWN:
        roi = (x, y, x, y)
    elif event == cv2.EVENT_MOUSEMOVE and roi:
        x1, y1, _, _ = roi
        roi = (x1, y1, x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        x1, y1, x2, y2 = roi
        roi = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

cv2.setMouseCallback("Select Object (Press 's' to Confirm)", select_roi)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if roi:
        x, y, w, h = roi
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Select Object (Press 's' to Confirm)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and roi:
        break

cv2.destroyWindow("Select Object (Press 's' to Confirm)")

# ✅ FIXED: Use legacy tracker
tracker = cv2.legacy.TrackerCSRT_create()
tracker.init(frame, roi)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, roi = tracker.update(frame)

    if success:
        x, y, w, h = map(int, roi)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Lost Tracking", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Live Object Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
