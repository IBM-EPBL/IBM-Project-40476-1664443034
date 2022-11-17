# import requests
# from flask import Flask, request,render_template
#
# app = Flask(__name__,template_folder='templates')
#
#
#
# @app.route('/city')
# def search_city():
#     API_KEY = 'your api key'  # initialize your key here
#     city = request.args.get('q')  # city name passed as argument
#
#     # call API and convert response into Python dictionary
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
#     response = requests.get(url).json()
#
#     # error like unknown city name, inavalid api key
#     if response.get('cod') != 200:
#         message = response.get('message', '')
#         return f'Error getting temperature for {city.title()}. Error message = {message}'
#
#     # get current temperature and convert it into Celsius
#     current_temperature = response.get('main', {}).get('temp')
#     if current_temperature:
#         current_temperature_celsius = round(current_temperature - 273.15, 2)
#         return f'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
#     else:
#         return f'Error getting temperature for {city.title()}'
#
#
# @app.route('/home/')
# def index():
#     return render_template('hotelWebsite.html')
#
# @app.route('/predict')
# def predictt():
#   return render_template('predict.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
#


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

# app = Flask(__name__)
# model = joblib.load('./Wind turbine.csv')

app = Flask(__name__)
try:
    model = joblib.load('Model_Predicted.sav')
    print(result)
except IndexError:

    print('list is empty')


@app.route('/')
def home():
    return render_template('intro.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/windapi',methods=['POST'])
def windapi():
    city=request.form.get('city')
    apikey="a12c4297bc4cc07edcaa3b4006273bbd"
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey
    resp = requests.get(url)
    resp=resp.json()
    temp = str((resp["main"]["temp"])-273.15) +" °C"
    humid = str(resp["main"]["humidity"])+" %"
    pressure = str(resp["main"]["pressure"])+" mmHG"
    speed = str((resp["wind"]["speed"])*3.6)+" Km/s"
    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed)
@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[float(x) for x in request.form.values()]]
    prediction = model.ppredict(x_test)
    print(prediction)
    output = prediction[0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))


if __name__ == "__main__":
     app.run(debug=False)
