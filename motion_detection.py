import winsound
import cv2
import imutils
import threading

# Video capturing
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Read the first frame
ret, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

# Initialize alarm variables
alarm = False
alarm_mode = False
alarm_counter = 0

# Function to sound the alarm
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("Alarm!")
        winsound.Beep(2500, 1000)
    alarm = False

# Main loop
while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        # Update the reference frame
        start_frame = frame_bw

        # Check for motion
        if threshold.sum() > 300:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Camera", threshold)

        # Trigger alarm if motion is consistent
        if alarm_counter > 20:
            if not alarm:
                alarm = True
                threading.Thread(target=beep_alarm).start()
    else:
        cv2.imshow("Camera", frame)

    # Key press handling
    key_pressed = cv2.waitKey(30)

    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0

    if key_pressed == ord("q"):
        alarm_mode = False
        break

# Release the camera and destroy windows
cap.release()
cv2.destroyAllWindows()