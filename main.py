from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
import os
import csv
app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]



line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    phrase = event.message.text.split(" ")
    csv_file = open("./iaafpt_m.csv", "r", encoding="utf_8",errors="",newline="")
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    if(phrase[0] == "HJ"):
        for row in f:
            if(row[0] == phrase[1]):
                textmessage = row[1]
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(phrase[0] +":"+ phrase[1] + "m \nIAAF得点は" + textmessage + "ptです"))

    if(phrase[0] == "PV"):
        for row in f:
            if(row[2] == phrase[1]):
                textmessage = row[3]
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(phrase[0] +":"+ phrase[1] + "m \nIAAF得点は" + textmessage + "ptです"))

    if(phrase[0] == "LJ"):
        for row in f:
            if(row[4] == phrase[1]):
                textmessage = row[5]
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(phrase[0] +":"+ phrase[1] + "m \nIAAF得点は" + textmessage + "ptです"))

    if(phrase[0] == "TJ"):
        for row in f:
            if(row[6] == phrase[1]):
                textmessage = row[7]
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(phrase[0] +":"+ phrase[1] + "m \nIAAF得点は" + textmessage + "ptです"))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("跳躍種目のIAAFptを返します! \n{種目} {記録} \nの順で入力してください"))







if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
