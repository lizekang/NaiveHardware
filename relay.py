#!flask/bin/python

from flask import Flask, jsonify, make_response, request, json
import httplib2
import json
app = Flask(__name__)


@app.route("/task", methods=['POST'])
def deploy():
    print(request.json[0])
    print(request.json[1]['device_ip'])
    print(request.json[2])
    print(request.json[3])
    device_ip = request.json[1]['device_ip']
    task_list = request.json[0]
    app_json = request.json[2]
    package_json = request.json[3]
    return jsonify({'errno': True})
    # headers = {"Content-type": "application/json"}
    # conn = httplib2.Http()
    # url = "http://" + device_ip + "/task"
    # resp, content = conn.request(url, 'POST',
    #                              headers=headers,
    #                              body=json.dumps(task_list))
    # if resp['status'] == '200':
    #     return jsonify({'errno': True})
    # else:
    #     return jsonify({'errno': False})
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)

