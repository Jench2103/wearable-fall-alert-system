from flask import render_template, url_for

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
