# camera_api.py
import threading
import time
import cv2
from flask import Flask, Response, jsonify
from pop import Util

app = Flask("camera_api")

# GStreamer 카메라 설정
cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)
cap = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    raise RuntimeError("Camera open failed")

latest_frame = None
stop_event = threading.Event()
frame_lock = threading.Lock()

def capture_loop():
    global latest_frame
    while not stop_event.is_set():
        ret, frame = cap.read()
        if ret:
            with frame_lock:
                latest_frame = frame.copy()
        time.sleep(0.01)

# JPG 압축률을 요구사항인 60%로 고정
def encode_jpeg(frame, quality=60):
    ret, jpeg = cv2.imencode(
        ".jpg",
        frame,
        [cv2.IMWRITE_JPEG_QUALITY, quality]
    )
    if not ret:
        return None
    return jpeg.tobytes()

@app.route("/")
def index():
    return """
    <html>
        <head><title>Jetson Camera API</title></head>
        <body>
            <h2>Jetson Camera API (60% Compression)</h2>
            <img src="/video" width="640" height="480">
            <p><a href="/snapshot.jpg">snapshot</a></p>
            <p><a href="/status">status</a></p>
            <p><a href="/stop">stop camera</a></p>
        </body>
    </html>
    """

@app.route("/video")
def video():
    def generate():
        while not stop_event.is_set():
            with frame_lock:
                frame = None if latest_frame is None else latest_frame.copy()

            if frame is None:
                time.sleep(0.05)
                continue

            jpg = encode_jpeg(frame, quality=60) # 60% 압축 적용
            if jpg is None:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
            )
            time.sleep(0.03)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/snapshot.jpg")
def snapshot():
    with frame_lock:
        frame = None if latest_frame is None else latest_frame.copy()
    if frame is None:
        return "No frame", 503
    jpg = encode_jpeg(frame, quality=60) # 60% 압축 적용
    return Response(jpg, mimetype="image/jpeg")

@app.route("/status")
def status():
    with frame_lock:
        frame = None if latest_frame is None else latest_frame.copy()
    if frame is None:
        return jsonify({"camera": "not ready"})
    h, w = frame.shape[:2]
    return jsonify({"camera": "ok", "width": w, "height": h})

@app.route("/stop")
def stop():
    stop_camera()
    return "camera stopped"

def stop_camera():
    stop_event.set()
    time.sleep(0.2)
    if cap.isOpened():
        cap.release()
    print("camera released")

def run_server():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True)

# 쓰레드 시작
capture_thread = threading.Thread(target=capture_loop)
capture_thread.start()

print("Camera API started")
print("Open: http://192.168.0.50:5000")

if __name__ == "__main__":
    run_server()