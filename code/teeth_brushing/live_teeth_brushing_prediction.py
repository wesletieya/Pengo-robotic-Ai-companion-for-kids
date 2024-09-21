import torch
import torch.nn as nn
from torchvision import transforms, models
import cv2
import numpy as np
from PIL import Image
import time

# Load the saved model
model_path = r'C:\Users\ayabe\vs projects\pengo\teeth_brusing\brushing_not_brushing_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# Define image transformations
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def predict_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        
    return predicted.item()

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

brushing_start_time = None
task_duration = 5  # 5 seconds
bravo_display_duration = 3  # Display "Bravo, kiddo!" for 3 seconds
bravo_display_start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize the frame for display purposes
    display_frame = cv2.resize(frame, (640, 480))
    
    # Predict the class
    pred_class = predict_image(frame)
    label = "brushing" if pred_class == 0 else "not brushing"
    
    # Check if brushing
    if label == "brushing":
        if brushing_start_time is None:
            brushing_start_time = time.time()
        elif time.time() - brushing_start_time >= task_duration:
            label = "Bravo, kiddo!"
            bravo_display_start_time = time.time()
            brushing_start_time = None
    else:
        brushing_start_time = None
    
    # Display the prediction and timer on the frame
    cv2.putText(display_frame, f"Label: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    if brushing_start_time is not None:
        time_elapsed = time.time() - brushing_start_time
        time_remaining = max(0, task_duration - time_elapsed)
        cv2.putText(display_frame, f"Timer: {int(time_remaining)}s", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    if bravo_display_start_time is not None:
        if time.time() - bravo_display_start_time >= bravo_display_duration:
            break
        cv2.putText(display_frame, "Bravo, kiddo!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Show the frame
    cv2.imshow('Video', display_frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
