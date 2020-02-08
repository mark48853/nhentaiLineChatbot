from flask import Flask , request , abort
import requests
import json
from Project.Config import *
from flask_cors import CORS
from flask_compress import Compress
from modules.nhentai import search,getBookById

app = Flask(__name__)
CORS(app)
Compress(app)


@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json


        Reply_token = payload['events'][0]['replyToken']
        message = payload['events'][0]['message']['text']
        print(message)
        book = json.loads(getBookById(message))
        print(book)

        for i in range (len(book["tags"])):
            print(book["tags"][i]["name"])
            # Reply_msg = book["tags"][i]["name"]
            # ReplyMessage(Reply_token,Reply_msg,Channel_access_token)
        title = book["title"]['english']
        Reply_msg = json.dumps(title)
        print(Reply_msg)
        ReplyMessage(Reply_token,Reply_msg,Channel_access_token)
        
        
        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello world',200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format('ACCESS TOKEN')
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
        "type": "text",
        "text": TextMessage
}]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200

if __name__ == "__main__":
    app.run(debug=True)