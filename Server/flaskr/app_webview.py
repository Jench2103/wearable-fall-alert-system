import json
from datetime import datetime, date

from flask import render_template, url_for, abort, flash
from flask import request

from flaskr.models import User, EmergencyEvent, DatabaseManager
from flaskr import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/article', methods=['GET'])
def article():
    return render_template('article.html')

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    var = {
        'username': '', 'name': '', 'gender':'', 'birthday': '', 'blood-type': '', 
        'hospital-city': '', 'hospital': ''
    }

    if request.method == 'POST':
        var['username'] = request.form.get('username')
        var['name'] = request.form.get('name')
        var['gender'] = request.form.get('gender')
        var['birthday'] = request.form.get('birthday')
        var['blood-type'] = request.form.get('blood-type')
        var['hospital-city'] = request.form.get('hospital-city')
        var['hospital'] = request.form.get('hospital')

        if var['username'] == None or len(var['username']) == 0 or var['username'].isspace():
            flash('帳號欄位請勿留白')
            return render_template('sign_up.html', var=var)

        try:
            new_user = User.create(var['username'], name=var['name'], sex=var['gender'], birthday=date.fromisoformat(var['birthday']), blood_type=var['blood-type'], hospital=var['hospital-city']+var['hospital'])
            flash('帳號建立成功！請返回 App 畫面登入')
        except:
            flash('帳號名稱已存在，請以其他帳號嘗試註冊，謝謝')

    return render_template('sign_up.html', var=var)

@app.route('/event/<token>', methods=['GET', 'POST'])
def event(token):
    if token == 'example':
        return render_template('event_example.html')

    try:
        event_object = EmergencyEvent.query.filter_by(web_token=token).first()
        user_object = User.query.get(event_object.user_id)
        event_location = json.loads(event_object.location)
        event_status = json.loads(event_object.event_status)
        
        if request.values.get('editable', None) == 'true':
            editable = True
        elif request.values.get('editable', None) == 'false':
            editable = False
        else:
            raise ValueError()

    except:
        abort(404)

    if request.method == 'POST':
        agency_type = request.values.get('agency-type', None)
        agency_name = request.values.get('agency-name', None)
        content = request.values.get('content', None)

        event_status.append({
            'time': datetime.now().strftime("%Y-%m-%d %H:%M"), 
            'type': agency_type, 
            'agency': agency_name, 
            'content': content
        })

        event_object.location = json.dumps(event_status, ensure_ascii=False)
        DatabaseManager.update(event_object)

    var = {
        'user': {'name': user_object.name, 'sex': user_object.sex, 'birthday': user_object.birthday},
        'event': {'time': event_object.time.strftime("%Y-%m-%d %H:%M"), 'gps': '', 'address': event_location['address']}, 
        'record': event_status.sort(key=lambda msg: datetime.strptime(msg['time'], '%Y-%m-%d %H:%M'), reverse=True) or [],
        'token': token, 'editable': editable
    }

    var['event']['gps'] = '{longitude}°E , {latitude}°N'.format(
        longitude=event_location['gps']['longitude'],
        latitude=event_location['gps']['latitude']
    )

    return render_template('event.html', var=var)
