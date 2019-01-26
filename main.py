from flask import Flask, render_template
import configparser

config = configparser.ConfigParser()
config.read('main_config.ini')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    flask_config = config['config']
    app.run(debug=flask_config['debug'], host=flask_config['host'], port=flask_config['port'])
