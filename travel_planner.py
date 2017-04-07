from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import json
import logging
from  sklearn.ensemble import GradientBoostingRegressor 

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/results',methods=['POST','GET'])
def results():
    if request.method=='POST':
        inputs = request.form

	#Load the pickled model
        time_model = pickle.load(open('pkl_time.pkl', 'rb'))
        base_fare_model = pickle.load(open('pkl_base_fare.pkl', 'rb'))

	try:
            is_yellow = inputs['is_yellow'][0]
        except:
            is_yellow = 1
        try:
            pu_latitude = inputs['pu_latitude'][0]
        except:
            pu_latitude = 40.75
        try:
            pu_longitude = inputs['pu_longitude'][0]
        except:
            pu_longitude = -73.97
        try:
            do_latitude = inputs['do_latitude'][0]
        except:
            do_latitude = 40.77
        try:
            do_longitude = inputs['do_longitude'][0]
        except:
            do_longitude = -73.95
	try:
	    pu_hour = inputs['pu_hour'][0]
	except:
	    pu_hour = 12
	try:
	    pu_day = inputs['pu_day'][0]
	except:
	    pu_day = 5
	try:
            trip_distance = inputs['trip_distance'][0]
	except:
	    trip_distance = 10 

	time_pred_array = np.array([is_yellow, pu_latitude,\
            pu_longitude, do_latitude, do_longitude, pu_hour, pu_day])

	trip_time = time_model.predict(time_pred_array)[0]

        base_fare_array = np.array([trip_distance, trip_time])

        base_fare = base_fare_model.predict(base_fare_array)[0]

        final_fare = base_fare

	return jsonify(trip_time, final_fare)


if __name__ == '__main__':
    '''Connects to the server'''

#    HOST = '127.0.0.1'
#    PORT = '4000'

#    app.run(HOST, PORT)
    app.run()