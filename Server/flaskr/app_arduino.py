from datetime import datetime, date
import requests
import json

from flask import abort, url_for
from flask import request
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from flaskr import app, line_bot_api
from flaskr.models import User, EmergencyContact, EmergencyEvent, AmbulanceInfo, DistrictAffairsInfo, LineToken

# constants
MODEL_CLASS_DICT = {
    'User': User, 
    'EmergencyContact':EmergencyContact,
    'AmbulanceInfo':AmbulanceInfo,
    'DistrictAffairsInfo': DistrictAffairsInfo
}


@app.route('/arduino/test', methods=['POST', 'GET'])
def arduino_test():
    """
    This view function provides a playground for developers to check what arguments 
    does the server actually received with requests. The returned string contains 
    arguments and corresponding values to the client for debugging.
    """
    print(request.args)
    return str(request.args.to_dict())


@app.route('/arduino/inviting-token', methods=['GET'])
def get_token():
    """
    Argument list:
        - type  : class that the invitation token belonging to
        - id    : object ID of the token owner
    
    Return value: intivation token for the specified object
    """
    class_name = request.args.get('type', None)
    owner_id = request.args.get('id', None)
    
    try:
        owner_object = MODEL_CLASS_DICT[class_name].query.get(owner_id)
    except:
        abort(404)

    token = LineToken.generate(type(owner_object).__name__, owner_object.id)
    return token


@app.route('/arduino/user/create', methods=['GET'])
def create_user():
    """
    Argument list:
        - username  : the username of new User account
        - name      : the name of new user
        - sex
        - birthday  : format the date string to 'YYYY-MM-DD'
        - blood_type
        - hospital  : prefer hospital
    
    Return value: ID of the new account
    """
    try:
        username = request.args.get('username', None)
        if username == None or len(username) == 0 or username.isspace():
            raise ValueError()
    except:
        abort(404)
    
    name = request.args.get('name', None)
    sex = request.args.get('sex', None)
    birthday = date.fromisoformat(request.args.get('birthday', None)) if request.args.get('birthday', None) else None
    blood_type = request.args.get('blood_type', None)
    hospital = request.args.get('hospital', None)

    try:
        new_user = User.create(username, name=name, sex=sex, birthday=birthday, blood_type=blood_type, hospital=hospital)
    except:
        abort(404)
    
    return str(new_user.id)


@app.route('/arduino/user/login', methods=['GET'])
def arduino_user_login():
    """
    Argument list:
        - username  : the username of new User account
    
    Return value example: 
        {
            'id': '12', 
            'name': 'Mr. Lee',
            'sex': 'Male',
            'birthday': '1970-01-01',
            'blood_type': 'A'
        }
    """
    try:
        username = request.args.get('username')
        user_id = User.query.filter_by(username=username).first().id
        user_object = User.query.get(user_id)
    except:
        abort(404)

    result = dict()

    result['id'] = str(user_object.id)
    result['name'] = user_object.name if user_object.name else 'None'
    result['sex'] = user_object.sex if user_object.sex else 'None'
    result['birthday'] = str(user_object.birthday) if user_object.birthday else 'None'
    result['blood_type'] = user_object.blood_type if user_object.blood_type else 'None'
    result['hospital'] = user_object.hospital if user_object.hospital else 'None'

    return json.dumps(result, ensure_ascii=False)


@app.route('/event/new', methods=['GET', 'POST'])
def new_event():
    """
    Argument list:
        - user_id
        - heart_rate
        - gps
    """

    try:
        user = User.query.get(int(request.args.get('user_id')))
        heart_rate = int(request.args.get('heart_rate'))
        gps_longitude = float(request.args.get('gps_longitude'))
        gps_latitude = float(request.args.get('gps_latitude'))
        phone_gps_longitude = float(request.args.get('phone_gps_longitude'))
        phone_gps_latitude = float(request.args.get('phone_gps_latitude'))

    except:
        abort(404)

    if gps_longitude == 0.0 or gps_latitude == 0:
        gps_longitude = phone_gps_longitude if phone_gps_longitude != 0.0 else 120.216792802224
        gps_latitude = phone_gps_latitude if phone_gps_latitude != 0.0 else 22.99887729057317

    gmap_response = requests.request(
        'get', 
        'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&language=zh-TW&key={key}'.format(
            latitude=str(gps_latitude), 
            longitude=str(gps_longitude), 
            key=app.config['GOOGLE_CLOUD_API_KEY']
        )
    )

    try:
        address = json.loads(gmap_response.text)['results'][0]['formatted_address']
    except:
        address = ''

    emergency_event = EmergencyEvent.create(
        user.id, 
        location={'gps': {'longitude': gps_longitude, 'latitude': gps_latitude}, 'address': address},
        user_status={'heart_rate': heart_rate}
    )

    linebot_message = {
        'emergency_contact': \
            ('【事件通報】您關注的使用者{name}在{datetime}於「{address}」附近' + \
            '發生疑似意外摔跌事件（GPS座標：{latitude}, {longitude}），系統已自動通報救護單位前往處置，' + \
            '並告知優先送治醫院：「{hospital}」，實際送治醫療院所以救護單位資訊為準。' + \
            '您可以利用 {url} 查看本次事件的最新狀態。').format(
                name=user.name, 
                datetime=emergency_event.time.strftime("%Y-%m-%d %H:%M"),
                address=address,
                latitude=str(gps_latitude), 
                longitude=str(gps_longitude), 
                hospital=user.hospital,
                url=url_for('event', token=emergency_event.web_token, editable='false', _external=True)
            )
    }

    for emergency_contact in (EmergencyContact.query.filter_by(user_id=user.id).all() or []):
        line_bot_api.push_message(emergency_contact.line_id, TextSendMessage(text=linebot_message['emergency_contact']))

    return str(emergency_event.web_token)
