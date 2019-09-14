import cv2

capture = cv2.VideoCapture('rtsp://hackathon:!Hackath0n@192.168.0.2:554/1')
print(capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT), capture.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter("output.mp4", -1, 60.0, (1280, 720)z)

while(True):
    ret, frame = capture.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # w = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    #resized = cv2.resize(gray, (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))), interpolation=cv2.INTER_LINEAR)
    if ret:
        #frame = cv2.flip(frame, 0)
        out.write(frame)
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
out.release()
cv2.destroyAllWindows()