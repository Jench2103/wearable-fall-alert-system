from flaskr import webview, linebot
from flaskr import app
from flaskr.models import db


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False)
