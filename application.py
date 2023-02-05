from flask import Flask, render_template, request, redirect
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
    return render_template('map/map.html', data=json.dumps(bigDict))

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
    index = 0
    error = None
    if request.method == 'POST':
        index = int(request.form['teacher'])
        teacherW = weights[index]
        index = int(request.form['crime'])
        crimeW = weights[index]
        index = int(request.form['climate'])
        climateW = weights[index]
        index = int(request.form['health'])
        healthW = weights[index]
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
                    'VT': 0, 'VA': 0, 'WA': 0, 'WV': 0, 'WI': 0, 'WY': 0, 'min': 0, 'max': 0}
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                linecount = 0
                for row in csv_reader:
                    if linecount == 1:
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

        statesEdu = parseCSV('db/education.csv', 1, teacherW)
        statesCrime = parseCSV('db/crime.csv', -1, crimeW)
        statesHealth = parseCSV('db/death.csv', -1, healthW)
        statesWeather = parseCSV('db/weather.csv', 1, climateW)

        state_names= [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY' ];

        max_score = 0
        min_score = 0
        for name in state_names:
            # Get the score from the current state
            score = states[name]

            # If the current score is greater than the maximum score, update max_score
            if score > max_score:
                max_score = score
            if score < min_score:
                min_score = score
        #bigDict['max_and_min'] = {'max' : max_score, 'min': min_score}
        for name in state_names:
            norm = (states[name] - min_score) / (max_score - min_score)
            bigDict[name] = {'crime': statesCrime[name], 'climate': statesWeather[name], 'health': statesHealth[name], 'education': statesEdu[name], 'score': states[name], 'norm': norm }
        # Store the results in a list
        results = []

        # For each state, compute the final score by summing up the scores from each category
        for name in state_names:
            score = states[name]
            results.append((name, score))

        # Sort the results in descending order
        results.sort(key=lambda x: x[1], reverse=True)

        # Display the top 5 states
        print("Top 5 states:")
        bigDict["top5"] = {results[0][0]: results[0][1],
            results[1][0]: results[1][1],
            results[2][0]: results[2][1],
            results[3][0]: results[3][1],
            results[4][0]: results[4][1],
        }
        for i in range(5):

            print("{0}. {1} ({2:.2f})".format(i+1, results[i][0], results[i][1]))


        print(max_score)
        print(min_score)
        return redirect('/map')

    return render_template('survey.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)