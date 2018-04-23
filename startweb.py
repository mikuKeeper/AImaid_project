from AImaid.expression.display.webview.webapi import live2d_talk
from flask import Flask,make_response
app = Flask(__name__)


@app.route('/webapi')
def index():
    return 'hello'

@app.route('/webapi/voice/fetchyuyin')
def fetchTalkURL():
    data = live2d_talk.getTextUrl()
    response = addHeaders(data)
    return response

def addHeaders(data):
    response = make_response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
