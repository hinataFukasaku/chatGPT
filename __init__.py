import logging
import os
import openai

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


channel_secret = 'f5dd6d3de9b20974f1691e54b552f00e'
channel_access_token = 'H8Hvd+UYZUWebVwwx9CMqEbeCJq8sEuoBQRr456AScvKT5+qz1434s1tfqbNkiN5ndj5y3Maa8vLQjgtfE40fNg46vsRFJqve5TXPbBl5exq4DBNwcjsg9G/Q6vnCy1yYhQXr8E/XrgxF+ImnTnawwdB04t89/1O/w1cDnyilFU='
openai.api_key = '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'

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get x-line-signature header value
    signature = req.headers['x-line-signature']

    # get request body as text
    body = req.get_body().decode("utf-8")
    logging.info("Request body: HttpTrigger1" + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        func.HttpResponse(status_code=400)

    return func.HttpResponse('OK')

def generate_response(message):
    # OpenAI APIを使用して返答を生成する

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": \
             "ここにチャットボットの設定を入れられます。\
             一人称や口調、会話例、行動指針などを指定すると その通りのチャットボットになります。"
             },
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    message = event.message.text
    response = generate_response(message)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )
