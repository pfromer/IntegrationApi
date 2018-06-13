from flask import Flask, jsonify, request, abort
import json, requests
from platforms import platforms
import sys, argparse
import logging

app = Flask(__name__)
headers = {'content-type': 'application/json'}

def check_valid_port(value):
    try:
      return int(value)
    except:
      raise argparse.ArgumentTypeError("%s is an invalid port" % value)

def getPlatformByToken(token):
    for platform in json.loads(platforms):
        if platform['token'] == request.json['token']:
            return platform['name']
    abort(401)

def forwardToPlatforms(platformName, method, data, toPlatforms):
    for platform in json.loads(platforms):
        if platform['name'] == platformName or (platform['name'] not in toPlatforms):
            return
        
        endpoint = platform['endpoint'] + method
        try:
            r = requests.post(url=endpoint, data=json.dumps(data), headers=headers, verify=False)
            app.logger.debug('Forwarded to {} :: {}'.format(platform['name'], r))
        except:
            app.logger.error('{} :: {}'.format(endpoint, sys.exc_info()))
            continue


def forwardToOhterPlatforms(platformName, method, data):
    for platform in json.loads(platforms):
        if platform['name'] == platformName:
            return
        endpoint = platform['endpoint'] + method
        try:
            r = requests.post(url=endpoint, data=json.dumps(data), headers=headers, verify=False)
            app.logger.debug('Forwarded to {} :: {}'.format(platform['name'], r))
        except:
            app.logger.error('{} :: {}'.format(endpoint, sys.exc_info()))
            continue
              


@app.route('/users', methods=['GET'])
def get_users():
    users = {}

    for platform in json.loads(platforms):
        endpoint = platform['endpoint'] + "users"
        platformName = platform['name']
        r = requests.get(url=endpoint, headers=headers, verify=False)
        users[platformName] = r.json()['users']
    
    app.logger.debug('Returning users.\n {}'.format(users))
    return jsonify({'users': users})


@app.route('/platforms', methods=['GET'])
def get_platforms():
    platformsList = []
    for platform in json.loads(platforms):
        endpoint = platform['endpoint'] + "users"
        jsonPlatform = {}
        try:
          r = requests.get(url=endpoint, headers=headers, verify=False)
          jsonPlatform['name'] = platform['name']
          jsonPlatform['users'] = r.json()['users']
          jsonPlatform['supportAudio'] = platform['supportAudio']
          jsonPlatform['supportImage'] = platform['supportImage']
          platformsList.append(jsonPlatform)
        except:
          app.logger.error('{} :: {}'.format(endpoint,sys.exc_info()))
          continue
    
    app.logger.debug('Returning platforms.\n {}'.format(platformsList))
    return jsonify({'platforms': platformsList})



@app.route('/user', methods=['POST'])
def new_user():
    if not request.json:
        app.logger.error('{}'.format(sys.exc_info()))
        abort(400)

    platformName = getPlatformByToken(request.json['token'])
    
    app.logger.debug('New user on the platform {}'.format(platformName))

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
	
    toPlatforms = []
    for obj in room['users']:
        toPlatforms.append(list(obj.keys())[0])

    forwardToPlatforms(platformName, "room", room, toPlatforms)
    return "success"


@app.route('/message', methods=['POST'])
def new_message():
    if not request.json:
        app.logger.error('{}'.format(sys.exc_info()))
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

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    for platform in json.loads(platforms):
        endpoint = platform['endpoint'] + "pong"
        try:
            r = requests.post(
              url=endpoint,
              data=json.dumps({'status': "pong"}),
              headers=headers,
              timeout=2,
              verify=False
            )
        except Exception:
            app.logger.error('{} :: {}'.format(endpoint,sys.exc_info()))
            pass
    return jsonify({'status': "ok", "message": "Sent \"pong\" to all platforms"})


if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'
    https = True
    
    parser = argparse.ArgumentParser(description='Lanza un IntegrationApi\
                                     en el puerto que recibe o en el 5000')
    parser.add_argument('-d', '--debug', action='store_true', help='Muestra debug')
    parser.add_argument('-s', '--https', action='store_true', help='Utiliza https')
    parser.add_argument('-p','--port', type=check_valid_port, default=port, required=False,
                        help='Puerto. Default {}'.format(port))

    args = parser.parse_args()
    
    if not args.https:
        app.run(host=host, port=args.port, debug=args.debug)

    else:
        app.run(host=host, port=args.port, debug=args.debug, ssl_context=('cert.pem', 'key.pem'))