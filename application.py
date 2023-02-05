from flask import Flask, render_template

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
    return render_template('map/map.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)