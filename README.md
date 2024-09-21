# Pengo-robotic-Ai-companion-for-kids

PENGO: A Robotic Kids Companion 🤖🌱
PENGO is an innovative AI-powered robotic companion designed to assist hyperactive children in managing daily tasks, building positive habits, and promoting well-being through interactive experiences. The robot offers a range of engaging features, including habit tracking, a child-friendly chatbot, and a smart garden that teaches responsibility.

Problem Statement
Hyperactive children often face challenges in maintaining focus, completing tasks, and staying calm. The need for consistent support and encouragement is critical to help these children navigate their daily routines and develop important life skills.

Solution
PENGO is a robotic companion designed to engage children through a reward system, encourage task completion, and provide calming activities. The robot is equipped with habit tracking, form detection, and storytelling, all presented in a kid-friendly, approachable manner.

Features
Habit Tracking: Detects and tracks tasks such as brushing teeth, rewarding children for task completion.
Child-Friendly Chatbot: Engages children with stories and conversations using voice interactions.
Form Detection: Helps children focus by providing challenges involving shape recognition and contour detection.
Smart Garden: Encourages responsibility by allowing children to take care of a real plant as part of a reward system.
System Design
Anthropomorphic Design: PENGO is designed with a cute penguin shape and child-friendly aesthetics to appeal to children.
Durable & Safe: Built with non-toxic materials, rounded edges, and secure compartments.
Key Components
ESP32 Board: Used for controlling the smart garden's watering system.
AI-Powered Processing: Detects tasks and habits in real-time.
Voice Interaction: Text-to-Speech (TTS) and Speech-to-Text (STT) for chatbot functionalities.
Habit Tracking (Brushing Teeth)
Using a custom ResNet-18 model, PENGO detects whether a child is brushing their teeth and rewards them upon task completion. The AI model was trained on a custom dataset collected using the Bing Image Downloader library. Real-time detection is achieved using a camera.

Form Detection
PENGO encourages kids to focus by detecting shapes drawn by them through a video feed. It uses OpenCV for contour detection and shape recognition.

Child-Friendly Chatbot
The chatbot uses a custom-built dataset of children’s questions and answers. It implements the Jaccard similarity function to find the best matching response and uses voice technologies like Microsoft Edge-TTS and Google Speech Recognition.

Smart Garden
Children are rewarded for completing tasks with the ability to water a real plant, teaching them responsibility. The garden system monitors soil humidity and activates a water pump when needed, controlled via the ESP32 board and Blynk app.

Future Expansions
Hand Washing Detection: Using AI to detect proper handwashing habits.
Obstacle Avoidance: Introducing features to navigate the physical environment safely.
Bad Words Detection: Teaching children appropriate language by detecting and correcting improper words.

Additional Details
You can find further details about the project by following this link: https://drive.google.com/drive/u/1/folders/1ffF29K20xKsrrQyMGXb-5nEQq11-Ff5n?fbclid=IwZXh0bgNhZW0CMTEAAR2UxMR_3kbe-pqHOmdxMqfHujarSXAbjbIamaOB_qs9Mq-BWGhKt_7_TxU_aem_BdYBRrClVXIcSPn5m3ulsw

