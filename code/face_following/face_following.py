# Loading Necessary Modules
import cv2
import time

# Variables
x, y, h, w = 0, 0, 0, 0
DISTANCE = 0

# Constants
INCH_TO_CM = 2.54

# Known measurements in inches, converted to centimeters
Known_distance = 31.5 * INCH_TO_CM  # cm
Known_width = 5.7 * INCH_TO_CM  # cm

# Colors  >>> BGR Format(BLUE, GREEN, RED)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)

fonts = cv2.FONT_HERSHEY_COMPLEX

cap = cv2.VideoCapture(0)
Distance_level = 0

# Face detector object
face_detector = cv2.CascadeClassifier(r"C:\Users\ayabe\Downloads\haarcascade_frontalface_default.xml")

# Focal length finder function
def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length

# Distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance

# Face detection function
def face_data(image, CallOut, Distance_level):
    face_width = 0
    face_center_x = 0
    face_center_y = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    for (x, y, h, w) in faces:
        face_width = w
        face_center_x = int(w / 2) + x
        face_center_y = int(h / 2) + y
        if Distance_level < 10:
            Distance_level = 10

        if CallOut:
            LLV = int(h * 0.12)
            line_thickness = 2

            cv2.line(image, (x, y + LLV), (x + w, y + LLV), GREEN, line_thickness)
            cv2.line(image, (x, y + h), (x + w, y + h), GREEN, line_thickness)
            cv2.line(image, (x, y + LLV), (x, y + LLV + LLV), GREEN, line_thickness)
            cv2.line(image, (x + w, y + LLV), (x + w, y + LLV + LLV), GREEN, line_thickness)
            cv2.line(image, (x, y + h), (x, y + h - LLV), GREEN, line_thickness)
            cv2.line(image, (x + w, y + h), (x + w, y + h - LLV), GREEN, line_thickness)

            cv2.line(image, (x, y), (face_center_x, face_center_y), (155, 155, 155), 1)
            cv2.line(image, (x, y - 11), (x + 210, y - 11), YELLOW, 25)
            cv2.line(image, (x, y - 11), (x + Distance_level, y - 11), GREEN, 25)

            cv2.circle(image, (face_center_x, face_center_y), 2, PURPLE, 1)
            cv2.circle(image, (x, y), 2, PURPLE, 1)

    return face_width, faces, face_center_x, face_center_y

# Reading reference image from directory
ref_image = cv2.imread(r"C:\Users\ayabe\Downloads\Ref_image.png")

ref_image_face_width, _, _, _ = face_data(ref_image, False, Distance_level)
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)

while True:
    _, frame = cap.read()
    frame_height, frame_width, _ = frame.shape
    RightBound = frame_width - 140
    Left_Bound = 140

    face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
    for (face_x, face_y, face_w, face_h) in Faces:
        if face_width_in_frame != 0:
            Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
            Distance = round(Distance, 2)
            Distance_level = int(Distance)

            cv2.line(frame, (50, 33), (130, 33), BLACK, 15)
            cv2.putText(frame, f"Distance {Distance} cm", (face_x - 6, face_y - 6), fonts, 0.6, BLACK, 2)
            
            if FC_X < Left_Bound:
                cv2.line(frame, (50, 65), (170, 65), BLACK, 15)
                cv2.putText(frame, f"Move Left {FC_X}", (50, 70), fonts, 0.4, YELLOW, 1)

            elif FC_X > RightBound:
                cv2.line(frame, (50, 65), (170, 65), BLACK, 15)
                cv2.putText(frame, f"Move Right {FC_X}", (50, 70), fonts, 0.4, GREEN, 1)

            elif Distance > 177.8 and Distance <= 508:  # 70 inches to 200 inches in cm
                cv2.line(frame, (50, 55), (200, 55), BLACK, 15)
                cv2.putText(frame, f"Forward Movement", (50, 58), fonts, 0.4, PURPLE, 1)

            elif Distance > 50.8 and Distance <= 177.8:  # 20 inches to 70 inches in cm
                cv2.line(frame, (50, 55), (200, 55), BLACK, 15)
                cv2.putText(frame, f"Backward Movement", (50, 58), fonts, 0.4, PURPLE, 1)

            else:
                cv2.line(frame, (50, 55), (200, 55), BLACK, 15)
                cv2.putText(frame, f"No Movement", (50, 58), fonts, 0.4, PURPLE, 1)

    cv2.line(frame, (Left_Bound, 80), (Left_Bound, 480 - 80), YELLOW, 2)
    cv2.line(frame, (RightBound, 80), (RightBound, 480 - 80), YELLOW, 2)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
