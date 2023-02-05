from flask import Flask, render_template, request
import csv
import json

bigDict = {}

app = Flask(__name__, 
    static_url_path='', 
    static_folder='static', 
    template_folder='templates')

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map/map.html', data=bigDict)

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/survey', methods=['POST','GET'])
def survey():
    weights = [.5, .75, 1.0, 1.25, 1.5]
    healthW = 1
    climateW = 1
    teacherW = 1
    crimeW = 1
    error = None
    if request.method == 'POST':
        if (request.form['health0']):
            healthW = weights[0]
        elif (request.form['health1']):
            healthW = weights[1]
        elif (request.form['health2']):
            healthW = weights[2]
        elif (request.form['health3']):
            healthW = weights[3]
        elif (request.form['health4']):
            healthW = weights[4]
        if (request.form['climate0']):
            climateW = weights[0]
        elif (request.form['climate1']):
            climateW = weights[1]
        elif (request.form['climate2']):
            climateW = weights[2]
        elif (request.form['climate3']):
            climateW = weights[3]
        elif (request.form['climate4']):
            climateW = weights[4]
        if (request.form['teacher0']):
            teacherW = weights[0]
        elif (request.form['teacher1']):
            teacherW = weights[1]
        elif (request.form['teacher2']):
            teacherW = weights[2]
        elif (request.form['teacher3']):
            teacherW = weights[3]
        elif (request.form['teacher4']):
            teacherW = weights[4]
        if (request.form['crime1']):
            crimeW = weights[0]
        elif (request.form['crime1']):
            crimeW = weights[1]
        elif (request.form['crime2']):
            crimeW = weights[2]
        elif (request.form['crime3']):
            crimeW = weights[3]
        elif (request.form['crime4']):
            crimeW = weights[4]
        states = {'AL': 0, 'AK': 0, 'AZ': 0, 'AR': 0, 'CA': 0, 'CO': 0, 'CT': 0, 'DE': 0, 'FL': 0, 'GA': 0, 'HI': 0,
                'ID': 0, 'IL': 0, 'IN': 0, 'IA': 0, 'KS': 0, 'KY': 0, 'LA': 0, 'ME': 0, 'MD': 0, 'MA': 0, 'MI': 0,
                'MN': 0, 'MS': 0, 'MO': 0, 'MT': 0, 'NE': 0, 'NV': 0, 'NH': 0, 'NJ': 0, 'NM': 0, 'NY': 0, 'NC': 0,
                'ND': 0, 'OH': 0, 'OK': 0, 'OR': 0, 'PA': 0, 'RI': 0, 'SC': 0, 'SD': 0, 'TN': 0, 'TX': 0, 'UT': 0,
                'VT': 0, 'VA': 0, 'WA': 0, 'WV': 0, 'WI': 0, 'WY': 0}
        
        def parseCSV(file, addsub, weight):
            statesReturn = {'AL': 0, 'AK': 0, 'AZ': 0, 'AR': 0, 'CA': 0, 'CO': 0, 'CT': 0, 'DE': 0, 'FL': 0, 'GA': 0, 'HI': 0,
                    'ID': 0, 'IL': 0, 'IN': 0, 'IA': 0, 'KS': 0, 'KY': 0, 'LA': 0, 'ME': 0, 'MD': 0, 'MA': 0, 'MI': 0,
                    'MN': 0, 'MS': 0, 'MO': 0, 'MT': 0, 'NE': 0, 'NV': 0, 'NH': 0, 'NJ': 0, 'NM': 0, 'NY': 0, 'NC': 0,
                    'ND': 0, 'OH': 0, 'OK': 0, 'OR': 0, 'PA': 0, 'RI': 0, 'SC': 0, 'SD': 0, 'TN': 0, 'TX': 0, 'UT': 0,
                    'VT': 0, 'VA': 0, 'WA': 0, 'WV': 0, 'WI': 0, 'WY': 0}
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                linecount = 0
                for row in csv_reader:
                    if linecount == 1:
                        #print(row)
                        max = float(row[0])
                    if linecount == 50:
                        min = float(row[0])
                    linecount += 1
                linecount = 0
                csv_file.seek(0)
                for row in csv_reader:
                    if linecount == 0:
                        pass
                    else:
                        statesReturn[row[1]] += addsub * (float(row[0]) * weight - min) / (max - min)
                        states[row[1]] += addsub * (float(row[0]) * weight - min) / (max - min)
                    linecount += 1
                return statesReturn

        #states += parseCSV('db/education.csv', 1, teacherW)
        #states += parseCSV('db/crime.csv', -1, crimeW)
        #states += parseCSV('db/death.csv', -1, healthW)
        #states += parseCSV('db/weather.csv', 1, climateW)
        statesEdu = parseCSV('db/education.csv', 1, teacherW)
        statesCrime = parseCSV('db/crime.csv', -1, crimeW)
        statesHealth = parseCSV('db/death.csv', -1, healthW)
        statesWeather = parseCSV('db/weather.csv', 1, climateW)



        print(statesEdu)
        print(statesCrime)
        print(statesHealth)
        print(statesWeather)
        state_names= [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ];

        for name in state_names:
            #print(key)
            bigDict[name] = {'crime': statesCrime[name], 'climate': statesWeather[name], 'health': statesHealth[name], 'education': statesEdu[name], 'score': states[name]}
        print(bigDict)

        return map(bigDict)

    return render_template('survey.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
