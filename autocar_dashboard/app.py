import os
import sys
import threading
import time
from flask import Flask, render_template, Response, jsonify, request
import cv2
from pop import Util, Pilot  # Pilot 라이브러리 정상 로드

app = Flask(__name__)

# --- [하드웨어 초기화] ---
car = Pilot.AutoCar()

# 카메라 각도 저장용 전역 변수 (초기값: 정면 90도, 살짝 아래 45도)
current_pan = 90
current_tilt = 45
last_servo_time = 0

# GStreamer 카메라 설정
Util.enable_imshow()
cam_pipeline = Util.gstrmer(width=640, height=480, fps=30)
camera = cv2.VideoCapture(cam_pipeline, cv2.CAP_GSTREAMER)

if not camera.isOpened():
    print("[경고] GStreamer 카메라를 열 수 없습니다!")
else:
    print("[성공] 카메라 파이프라인이 정상적으로 열렸습니다.")

# --- [카메라 스트리밍 영상 송출] ---
def generate_frames():
    while True:
        if not camera.isOpened():
            time.sleep(0.5)
            continue
            
        success, frame = camera.read()
        if not success:
            time.sleep(0.1)
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('dashboard.html')

# --- [조이스틱 제어 API: 완벽한 주행/정지 보정 적용] ---
@app.route('/api/move', methods=['POST'])
def move_car():
    data = request.json
    x = data.get('x', 0)  # 조향 값 (-100 ~ 100)
    y = data.get('y', 0)  # 속도 값 (-100 ~ 100)
    
    try:
        # 안전장치: 조이스틱 값이 중심(0) 근처면 확실하게 STOP 명령 인지
        if -15 <= y <= 15:
            car.stop()
        elif y > 15:
            car.forward(int(y))
        elif y < -15:
            car.backward(int(abs(y)))
            
        # 조향 제어 오차 보정
        if -15 <= x <= 15:
            car.steering = 0
        else:
            car.steering = int(x)
            
        print(f"[주행] 속도: {y}, 조향: {x}")
    except Exception as e:
        print(f"모터 제어 오류: {e}")
        
    return jsonify({"status": "success"})

# --- [카메라 정밀 1도 단위 제어 API] ---
@app.route('/api/camera', methods=['POST'])
def control_camera():
    global current_pan, current_tilt, last_servo_time
    data = request.json
    direction = data.get('direction', '')
    
    # 0.02초 이내로 너무 빠르게 들어오는 연타 신호는 하드웨어 보호를 위해 컷!
    now = time.time()
    if now - last_servo_time < 0.02:
        return jsonify({"status": "ignored", "pan": current_pan, "tilt": current_tilt})
    last_servo_time = now

    step = 1  # 정밀하게 딱 1도씩 무빙
    
    if direction == 'left':
        current_pan += step
    elif direction == 'right':
        current_pan -= step
    elif direction == 'up':
        current_tilt += step
    elif direction == 'down':
        current_tilt -= step

    # 완벽 마지노선 가이드 범위 제한 적용
    current_pan = max(0, min(180, current_pan))    # 좌우: 0 ~ 180도
    current_tilt = max(0, min(90, current_tilt))    # 위아래: 0 ~ 90도
    
    try:
        car.camPan(int(current_pan))
        car.camTilt(int(current_tilt))
        print(f"[카메라 정밀제어] {direction} -> Pan: {current_pan}°, Tilt: {current_tilt}°")
    except Exception as e:
        print(f"카메라 서보모터 구동 실패: {e}")
        
    return jsonify({"status": "success", "pan": current_pan, "tilt": current_tilt})

# --- [TTS API] ---
@app.route('/api/tts', methods=['POST'])
def play_tts():
    data = request.json
    text = data.get('text', '')
    def Speak():
        if text == "멜로디 재생":
            os.system("speaker-test -t sine -f 440 -l 1 > /dev/null 2>&1")
        else:
            try:
                from gtts import gTTS
                tts = gTTS(text=text, lang='ko')
                tts.save("alert.mp3")
                os.system("mpg321 alert.mp3 > /dev/null 2>&1")
            except:
                pass
    threading.Thread(target=Speak).start()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    try:
        print("포트 5000에서 하드웨어 안전 패치 적용 Flask 서버를 시작합니다...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        car.stop()
        if camera.isOpened():
            camera.release()