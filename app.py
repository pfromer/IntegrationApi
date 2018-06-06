from flask import Flask, jsonify, request, abort
import json
import requests
from platforms import platforms

app = Flask(__name__)
headers = {'content-type': 'application/json'}

@app.route('/users', methods=['GET'])
def get_users():
    users = {}

    for platform in json.loads(platforms):
        endpoint = platform['endpoint'] + "users"
        platformName = platform['name']
        r = requests.get(url=endpoint, headers=headers)
        users[platformName] = r.json()
    return jsonify({'users': users})



@app.route('/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)

    for platform in json.loads(platforms):
        if platform['token'] == request.json['token']:
            platformName = platform['name']

    user = {
        "id": request.json['id'],
        "name": request.json['name'],
        "platform": platformName
    }

    for platform in json.loads(platforms):
        if platform['token'] != request.json['token']:
            endpoint = platform['endpoint'] + "user"
            requests.post(url=endpoint, data=json.dumps(user), headers=headers)
    return "success"



@app.route('/room', methods=['POST'])
def new_room():
    if not request.json:
        abort(400)

    for platform in json.loads(platforms):
        if platform['token'] == request.json['token']:
            platformName = platform['name']

    room = {
        "id": request.json['id'],
        "name": request.json['name'],
        "platform": platformName,
        "users": request.json['users'],
        "type": request.json['type']
    }

    for platform in json.loads(platforms):
        if platform['token'] != request.json['token']:
            endpoint = platform['endpoint'] + "room"
            requests.post(url=endpoint, data=json.dumps(room), headers=headers)
    return "success"



@app.route('/message', methods=['POST'])
def new_message():
    if not request.json:
        abort(400)

    message = {
        "roomOriginalPlatform": request.json['roomOriginalPlatform'],
        "roomId": request.json['roomId'],
        "senderId": request.json['senderId'],
        "senderPlatform": request.json['senderPlatform'],
        "text": request.json['text']
    }

    for platform in json.loads(platforms):
        endpoint = platform['endpoint'] + "message"
        requests.post(url=endpoint, data=json.dumps(message), headers=headers)
    return "success"


if __name__ == '__main__':
    app.run()