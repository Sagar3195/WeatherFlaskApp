from flask import Flask, request, render_template, abort
#Importing json library to load the Json data to python dictionary
import json

#urllib.request to make request to api
import  urllib.request

app = Flask(__name__)

#Create function to convert temperature from Kelvin to degree celsius.
def degree_celsius(temp):
    return str(round(float(temp) - 273.15, 2))

@app.route('/', methods = ['POST', 'GET'])
def weather():
    #Your API Key will come here
    api_key = '5cc1946f62646c49e5b50d0246d51732'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #we use default city name
        city = 'Mumbai'

    # source conatin json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key).read()

    except:
        return abort(404)

    #Now converting json data into dictionary
    list_of_data = json.loads(source)

    #data for variable list of data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp_kelvin": str(list_of_data['main']['temp']) + 'K',
        "temp_celsius": degree_celsius(list_of_data['main']['temp']) + 'C',
        "pressure": str(list_of_data['main']['pressure']) + 'Pa',
        "humidity": str(list_of_data['main']['humidity']) + '%',
        "cityname": str(city)
    }

    return render_template('index.html', data = data)

if __name__ == '__main__':
    app.run(debug= True)