from flask import Flask, jsonify, request, abort
import json
import requests
from platforms import platforms
import sys, argparse

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


def check_valid_port(value):
    try:
      return int(value)
    except:
      raise argparse.ArgumentTypeError("%s is an invalid port" % value)

if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'
    https = True
    
    parser = argparse.ArgumentParser(description='Lanza un IntegrationApi\
                                     en el puerto que recibe o en el 5000')
    parser.add_argument('-s', '--https', action='store_true', help='Utiliza https')
    parser.add_argument('-p','--port', type=check_valid_port, default=port, required=False,
                        help='Puerto. Default {}'.format(port))

    args = parser.parse_args()
    
    if not args.https:
        app.run(host=host, port=args.port)

    else:
        app.run(host=host, port=args.port, ssl_context=('cert.pem', 'key.pem'))