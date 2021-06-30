from flask import Flask, render_template, Response
from threading import Thread
from GraphicAndDetect_debug import Camera
import Vender

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('stream.html')

cam_wrapper = []

def gen():
    while 1:
        frame = cam_wrapper[0].get_frame()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def web_server():
    app.run(host='0.0.0.0', port=80, debug=False)

if __name__ == "__main__":
    t = Thread(target=web_server, args=())
    t.daemon = True
    t.start()
    cam_wrapper.append(Camera())

# vending machine
    vender = Vender.Vender(cam_wrapper[0])
    vender.run()
