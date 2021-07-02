import os

# 引入套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
# 引入 linebot 異常處理
from linebot.exceptions import(
    InvalidSignatureError
)
# 引入 linebot 訊息元件
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.models.send_messages import ImageSendMessage

app = Flask(__name__)

# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 此為 Webhook callback endpoint
@app.route("/callback", methods=['POST'])
def callback():
    # 取得網路請求的標頭 X-Line-Signature 內容，確認請求是從 Line Server 送來的
    signature = request.headers['X-Line-Signature']

    # 將請求內容取出
    body = request.get_data(as_text=True)

    # handle webhook body ( 轉送給負責處理的 handler，ex. handle_message)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channael access token/channel secret.")
        abort(400)

    return 'OK'

# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。 所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = TextSendMessage(text='請輸入正確指令')

    # 根據使用者輸入 event.message.text 條件判斷要回應哪一種訊息
    if user_message == '文字':
        reply_message = TextSendMessage(text=event.message.text)
    elif user_message == '圖片':
        reply_message == ImageSendMessage(
            original_content_url='https://example.com/original.jpg',
            preview_image_url='https://example.com/preview.jpg'
        )
    elif user_message == '貼圖':
        # pass
        pass
    elif user_message == '快速選單':
        pass
    line_bot_api.reply_message(
        event.reply_token,
        reply_message)

# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__
if __name__ == "__main__":
    # 運行 Flask Server，設定監聽 port 8080 ( 網路 IP 位置搭配 Port  可以辨識出要把網路請求送到那邊 xxx.xxx.xxx.xxx:port，0.0.0.0 代表任何 IP )
    app.run(host='0.0.0.0', port=8080)