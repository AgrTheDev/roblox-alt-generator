from flask import Flask, render_template, request
import requests, random
from waitress import serve

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
  return render_template('index.html')

@app.post('/authTicket')
def authTicket():
    cookie = request.args.get('cookie')
    gameid = request.args.get('gameid')
    with requests.session() as session:
        session.cookies['.ROBLOSECURITY'] = cookie
        session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
        xsrf_token = session.post('https://auth.roblox.com/v1/authentication-ticket/', headers={'referer':f'https://www.roblox.com/games/{gameid}'}).headers['rbx-authentication-ticket']
        browserId = random.randint(1000000, 10000000)
        return f'roblox-player:1+launchmode:play+gameinfo:{xsrf_token}+launchtime:{browserId}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browserId}%26placeId%3D{gameid}%26isPlayTogetherGame%3Dfalse+browsertrackerid:{browserId}+robloxLocale:en_us+gameLocale:en_us+channel:'

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
    print('a')
