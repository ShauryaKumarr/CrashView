from flask import Flask, Response, send_from_directory
import serial
import os

app = Flask(__name__)
ser = serial.Serial('/dev/tty.usbmodem11301', 115200)  # Replace with your port

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'serial_view.html')

@app.route('/data')
def stream():
    def generate():
        while True:
            line = ser.readline().decode('utf-8')
            yield f"data:{line}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)