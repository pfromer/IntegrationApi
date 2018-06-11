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
        users[platformName] = r.json()['users']
    return jsonify({'users': users})


@app.route('/platforms', methods=['GET'])
def get_platforms():
    platformsList = []

    for platform in json.loads(platforms):
        endpoint = platform['endpoint'] + "users"
        jsonPlatform = {}
        r = requests.get(url=endpoint, headers=headers)
        jsonPlatform['name'] = platform['name']
        jsonPlatform['users'] = r.json()['users']
        jsonPlatform['supportAudio'] = platform['supportAudio']
        jsonPlatform['supportImage'] = platform['supportImage']
        platformsList.append(jsonPlatform)
    return jsonify({'platforms': platformsList})



@app.route('/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)

    platformName = getPlatformByToken(request.json['token'])

    user = {
        "id": request.json['id'],
        "name": request.json['name'],
        "platform": platformName
    }

    forwardToOhterPlatforms(platformName, "user", user)
    return "success"



@app.route('/room', methods=['POST'])
def new_room():
    if not request.json:
        abort(400)

    platformName = getPlatformByToken(request.json['token'])

    room = {
        "id": request.json['id'],
        "name": request.json['name'],
        "platform": platformName,
        "users": request.json['users'],
        "type": request.json['type']
    }

    forwardToOhterPlatforms(platformName, "room", room)
    return "success"


@app.route('/message', methods=['POST'])
def new_message():
    if not request.json:
        abort(400)

    platformName = getPlatformByToken(request.json['token'])

    message = {
        "roomOriginalPlatform": request.json['roomOriginalPlatform'],
        "roomId": request.json['roomId'],
        "senderId": request.json['senderId'],
        "senderPlatform": platformName,
        "text": request.json['text']
    }

    forwardToOhterPlatforms(platformName, "message", message)
    return "success"

def getPlatformByToken(token):
    for platform in json.loads(platforms):
        if platform['token'] == request.json['token']:
            return platform['name']
    abort(401)

def forwardToOhterPlatforms(platformName, method, data):
    for platform in json.loads(platforms):
        if platform['name'] != platformName:
            endpoint = platform['endpoint'] + method
            requests.post(url=endpoint, data=json.dumps(data), headers=headers)



if __name__ == '__main__':
    app.run()