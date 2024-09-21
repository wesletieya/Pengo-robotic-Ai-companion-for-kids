import cv2
import mediapipe as mp
import time

# Settings
maximum_time = 15 # Seconds

# Load Face Detector
face_detection = mp.solutions.face_detection.FaceDetection()

# Take frame from capera
cap = cv2.VideoCapture(0)

# Track TIME
starting_time = time.time()


while True:
    # Take frame from camera
    ret, frame = cap.read()
    height, width, channels = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw rectangle
    cv2.rectangle(frame, (0, 0), (width, 70), (10, 10, 10), -1)

    # Face Detection
    results = face_detection.process(rgb_frame)

    # Is the face DETECTED?
    if results.detections:
        elapsed_time = int(time.time() - starting_time)

        if elapsed_time > maximum_time:
            # Reached maximum time, show alert
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 225), 10)
            cv2.setWindowProperty("Frame", cv2.WND_PROP_TOPMOST, 1)

        # Draw elapsed time on screen
        cv2.putText(frame, "{} seconds".format(elapsed_time), (10, 50), cv2.FONT_HERSHEY_PLAIN,
                    3, (15, 225, 215), 2)
        print("Elapsed: {}".format(elapsed_time))
        print("Face looking at the screen")
    else:
        print("NO FACE")
        # Reset the counter
        starting_time = time.time()

    # Display frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()