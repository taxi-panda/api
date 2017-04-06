from flask import Flask
from flask import request
import logging
from logging.handlers import TimedRotatingFileHandler
import json


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = TimedRotatingFileHandler('test.log', when='d', interval=1, backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

app = Flask(__name__)

@app.route('/')
def hello_world():
    logger.debug('Default route')
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict_stuff():
    logger.debug('Predict route called')

    name = request.form['name']
    age = request.form['age']
    name_len = len(name)

    logger.debug('Received the following params:' + str(name) + ' and ' + str(age))

    my_dict = {'user_name': name, 'name_length': name_len, 'user_age': age}

    return json.dumps(my_dict)

if __name__ == '__main__':
    app.run()
