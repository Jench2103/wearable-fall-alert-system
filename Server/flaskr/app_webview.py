import json
from datetime import datetime

from flask import render_template, url_for, abort
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
