from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move/<direction>')
def move(direction):
    print(f"\n[명령 수신] RC카가 {direction} 방향으로 움직입니다!")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)