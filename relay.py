#!flask/bin/python

from flask import Flask, jsonify, make_response, request, json
import httplib2
import json
import hashlib
import urllib.request as req

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
    print(request.json[0]['device_ip'])
    print()
    print(request.json[1])
    print()
    print(request.json[2])
    print()
    print(request.json[3])
    print()
    print(request.json[4])
    print()
    device_ip = request.json[0]['device_ip']
    task_list = request.json[1]
    driver = request.json[2]
    app_json = request.json[3]
    package_json = request.json[4]
    user_json = request.json[5]
    # with open("./task-list1.json", "w") as fp:
    #     fp.write(jsonify(str(task_list)))
    # with open("./drivers1.json", "w") as fp:
    #     fp.write(jsonify(str(driver)))
    with open("./user.json", "r") as fp:
        user = json.loads(fp.read())
    # with open("./drivers.json", "r") as fp:
    #     driver = json.loads(fp.read())
    # with open("./task-list.json", "r") as fp:
    #     task_list = json.loads(fp.read())
    if user_json['username'] == user['username'] and check_password(user['password'], user_json['password']):
        post = json.dumps([task_list, driver, app_json, package_json]).encode()
        # headers = {"Content-type": "application/json"}
        # conn = httplib2.Http()
        # url = "http://" + device_ip
        # resp, content = conn.request(url, 'POST',
        #                              headers=headers,
        #                              body=json.dumps([task_list,
        #                                               driver,
        #                                               app_json,
        #                                               package_json]).encode())
        url = "http://192.168.43.111:3000"
        req.urlopen(url, data=post)
        return jsonify({'errno': True})
        # return jsonify({'errno': True})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8081)



