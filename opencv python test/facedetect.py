import cv2
import time

# Import the face detection haar file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Init flags with their default values
showVideo = True
textOutput = False
showAr = True
showLine = False
zoomFace = False

# Init the camera and the window
cam = cv2.VideoCapture(0)
cv2.namedWindow('VideoOutput')

# Main Loop
while(True):
    # This is used to store the index of the largest face found
    # This is considered in later code to be the face of interest
    largestFaceIdx = -1

    # This block grabs an image from the camera and prepares
    # a grey version to be used in the face detection.
    (ret,frame) = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Run the face detection, and then check if any faces were found
    # faceFound is used later to skip certain section if there is no
    # face found in the input
    faces = face_cascade.detectMultiScale(gray, 2, 5)
    if (len(faces) > 0):
        faceFound = True
    else:
        faceFound = False

    # Output text to stdout
    if(textOutput and faceFound):
        largest = 0
        largestArea = 0
        for idx,(x,y,w,h) in enumerate(faces):
            if (w*h > largestArea):
                largestArea = w*h
                largestFaceIdx = idx
        print "pos : %r %r" % (largest,faces[largestFaceIdx])

    # Add boxes and lines as an overlay
    if (showAr and showVideo and faceFound):
        for idx,(x,y,w,h) in enumerate(faces):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(frame,"[%r]" % idx, (x , y - 5), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,0,0), 2)
            if (showLine):
                cv2.line(frame,(int(cam.get(3)/2),int(cam.get(4)/2)),(x + w/2, y + h/2),(255,0,0),4)

    # Zoom in on the primary face
    if (zoomFace and faceFound):
        (x,y,w,h) = faces[largestFaceIdx]
        zoom = frame[y:y+h, x:x+w]
        frame = cv2.resize(zoom,(int(cam.get(3)),int(cam.get(4))))

    # Output the video
    if (showVideo):
        cv2.imshow('VideoOutput', frame)

    # Check for keypresses
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
		break
    if key == ord("v"):
        showVideo = not showVideo
    if key == ord("t"):
        textOutput = not textOutput
    if key == ord("b"):
        showAr = not showAr
    if key == ord("l"):
        showLine = not showLine
    if key == ord("z"):
        zoomFace = not zoomFace

print "Quitting..."
cam.release()
cv2.destroyAllWindows()
