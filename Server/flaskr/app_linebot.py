from flask import request, abort

from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from flaskr import app, line_bot_api, line_bot_handler
from flaskr.models import User, EmergencyContact, EmergencyEvent, AmbulanceInfo, DistrictAffairsInfo, LineToken


@app.route("/linebot", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_bot_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@line_bot_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    match_token = LineToken.get_match_token(event.message.text)
    
    if match_token:
        if match_token.owner_class_name == 'User':
            user = User.query.get(match_token.owner_object_id)
            EmergencyContact.create(user.id, line_id=event.source.user_id)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text='您已經成功註冊為 {name} 的緊急連絡人'.format(name=user.name)
            ))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
