import numpy as np
import cv2 as cv
from images_stack import *
from thresholds_trackbars import *
import random


capture = cv.VideoCapture(0, cv.CAP_DSHOW) 
#def get_user_input():
 #   print("Enter the number of shapes you want to draw:")
  #  num_circles = int(input("Number of circles: "))
   # num_triangles = int(input("Number of triangles: "))
    #num_rectangles = int(input("Number of rectangles: "))
    #num_squares = int(input("Number of squares: "))
    #return num_circles, num_triangles, num_rectangles, num_squares

def define_numb_forms():
        num_circles = random.randint(0, 1)
        num_triangles =  random.randint(0, 1)
        num_rectangles = random.randint(0, 1)
        num_squares = 0
        print("These are the shapes you kiddo should draw: num_circles = ",num_circles, ", num_triangles = ", num_triangles," , num_rectangles = ",num_rectangles,' num_squares = ', num_squares)
        return num_circles, num_triangles, num_rectangles, num_squares 
#user_num_circles, user_num_triangles, user_num_rectangles, user_num_squares = get_user_input()
num_circles_def,num_triangles_def,num_rectangles_def,num_squares_def=define_numb_forms()

threshold_trackbars_create()


while True:
    # Capture frame-by-frame
    ret, frame = capture.read()

    # Trackbars Values
    blur, b, c, area, epsilon = threshold_trackbars_pos()

    # Frame Operations
    frame = cv.resize(frame, (500, 400))
    frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_blur = cv.medianBlur(frame_grey, blur)
    frame_threshold = cv.adaptiveThreshold(frame_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, b, c)

    # Get the contours
    font_face = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5

    num_circles = 0
    num_triangles = 0
    num_rectangles = 0
    num_squares = 0

    contours, _ = cv.findContours(frame_threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour_index in range(len(contours)):
        # Check if the contour is relevant
        if cv.contourArea(contours[contour_index], True) > area:
            # Number of Corners
            perimeter = cv.arcLength(contours[contour_index], True)
            poly = cv.approxPolyDP(contours[contour_index], epsilon * perimeter, True)
            bbox_x, bbox_y, bbox_w, bbox_h = cv.boundingRect(poly)
            cv.rectangle(frame, (bbox_x, bbox_y), (bbox_x + bbox_w, bbox_y + bbox_h), (0, 0, 0), 2)

            num_corners = len(poly)
            if num_corners == 3:
                cv.putText(frame, "Triangle", (bbox_x, bbox_y - 10), font_face, font_scale, (0, 0, 0), 1)
                num_triangles += 1
            elif num_corners == 4:
                if 0.95 <= bbox_w / bbox_h <= 1.05:
                    cv.putText(frame, "Square", (bbox_x, bbox_y - 10), font_face, font_scale, (0, 0, 0), 1)
                    num_squares += 1
                else:
                    cv.putText(frame, "Rectangle", (bbox_x, bbox_y - 10), font_face, font_scale, (0, 0, 0), 1)
                    num_rectangles += 1
            else:
                cv.putText(frame, "Circle", (bbox_x, bbox_y - 10), font_face, font_scale, (0, 0, 0), 1)
                num_circles += 1

    # Display the resulting stack
    cv.putText(frame, f"Triangles: {num_triangles}", (20, 20), font_face, font_scale, (0, 0, 0), 1)
    cv.putText(frame, f"Rectangles: {num_rectangles}", (20, 40), font_face, font_scale, (0, 0, 0), 1)
    cv.putText(frame, f"Squares: {num_squares}", (20, 60), font_face, font_scale, (0, 0, 0), 1)
    cv.putText(frame, f"Circles: {num_circles}", (20, 80), font_face, font_scale, (0, 0, 0), 1)
    # Compare detected shapes with user input
    correct = (
        num_circles == num_circles_def and
        num_triangles == num_triangles_def and
        num_rectangles == num_rectangles_def and
        num_squares == num_squares_def
    )
    if correct:
        cv.putText(frame, "Correct Drawing!", (20, 100), font_face, font_scale, (0, 255, 0), 2)
        print('sahitek')
        break
    else:
        cv.putText(frame, "Incorrect Drawing!", (20, 100), font_face, font_scale, (0, 0, 255), 2)


    stack = stack_images(1, [[frame, frame_grey], [frame_blur, frame_threshold]])
    cv.imshow("frame", stack)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
capture.release()
cv.destroyAllWindows()