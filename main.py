# perfect
import os
from cvzone.HandTrackingModule import HandDetector
import cv2     
import numpy as np


# Set up video capture
cap = cv2.VideoCapture(0)  # Change to 0 if you encounter issues with index 1
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
imgBackground = cv2.imread("Resources/Background.png")

# Path for mode images
folderPathModes = "Resources/Modes"
if not os.path.exists(folderPathModes):
    print(f"Error: The directory {folderPathModes} does not exist.")
    exit()

# Import all mode images to a list
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []

for imgModePath in listImgModesPath:
    img = cv2.imread(os.path.join(folderPathModes, imgModePath))
    if img is not None:  # Check if the image was loaded successfully
        listImgModes.append(img)
    else:
        print(f"Warning: {imgModePath} could not be loaded.")

print(listImgModes)

# Path for icons
folderPathIcons = "Resources/Icons"
if not os.path.exists(folderPathIcons):
    print(f"Error: The directory {folderPathIcons} does not exist.")
    exit()

# Import all icons to a list
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconsPath:
    img = cv2.imread(os.path.join(folderPathIcons, imgIconsPath))
    if img is not None:  # Check if the image was loaded successfully
        listImgIcons.append(img)
    else:
        print(f"Warning: {imgIconsPath} could not be loaded.")

modeType = 0  # For changing selection mode
selection = -1
counter = 0
selectionSpeed = 7
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]

while True:
    success, img = cap.read()
    if not success:
        print("Error: Unable to read from camera.")
        break

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    # Overlaying the webcam feed on the background image
    imgBackground[139:139 + 480, 50:50 + 640] = img
    imgBackground[0:720, 847: 1280] = listImgModes[modeType]

    if hands and counterPause == 0 and modeType < 3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0
        
    if counter > 0:
            counter += 1
            print(counter)
            cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0,
                        counter * selectionSpeed, (0, 255, 0), 20)
            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1
    
    # To pause after each selection is made
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0
    
    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

    # Displaying
    cv2.imshow("Background", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Add a way to exit the loop
        break

# Release resources
cap.release()
cv2.destroyAllWindows()