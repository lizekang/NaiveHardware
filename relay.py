#!flask/bin/python

from flask import Flask, jsonify, make_response, request, json
import httplib2
import json
import hashlib

app = Flask(__name__)
site_settings = {
    "salt_length": 12
}


def check_password(request_pwd, final_pwd):
    salt = final_pwd[:site_settings["salt_length"]]
    encoded_pwd = final_pwd[site_settings["salt_length"]:]
    request_new_pwd = salt + request_pwd + salt
    request_encoded_pwd = hashlib.sha256(request_new_pwd.encode('utf8'))\
        .hexdigest()
    if request_encoded_pwd == encoded_pwd:
        return True
    else:
        return False


@app.route("/task", methods=['POST'])
def deploy():
    print(request.json[0])
    print(request.json[1]['device_ip'])
    print(request.json[2])
    print(request.json[3])
    print(request.json[4])
    device_ip = request.json[1]['device_ip']
    task_list = request.json[0]
    app_json = request.json[2]
    package_json = request.json[3]
    user_json = request.json[4]
    with open("./user.json", "r") as fp:
        user = json.loads(fp.read())
    if user_json['username'] == user['username'] and check_password(user['password'], user_json['password']):
        print(True)
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



