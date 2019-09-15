from flask import Flask, render_template, request, Response
from flask_cors import CORS
from command_interpreter import CommandInterpreter
import cv2

app = Flask(__name__)
cors = CORS(app)

vcap = cv2.VideoCapture('../output_left1pink.mp4')


@app.route("/", methods=['GET', 'OPTIONS'])
def home():
    ci = CommandInterpreter()
    data = request.args.get("command")
    ci.interpreter(data)
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def generate():
    # loop over frames from the output stream
    while vcap.isOpened():
        ret, frame = vcap.read()
        ()
        # wait until the lock is acquired
        # with lock:
        #     # check if the output frame is available, otherwise skip
        #     # the iteration of the loop
        #     if outputFrame is None:
        #         continue

        # encode the frame in JPEG format
        if frame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        cv2.waitKey(22)
        # ensure the frame was successfully encoded
        if not flag:
            continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) +
               b'\r\n')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
