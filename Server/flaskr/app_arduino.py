from flask import request

from flaskr import app


@app.route('/arduino-test', methods=['POST'])
def arduino_test():
    print(request.args)
