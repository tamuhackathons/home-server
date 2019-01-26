from flask import Flask, render_template, jsonify
from plugins.plugin_parser import create_dictionary
import configparser

config = configparser.ConfigParser()
config.read('main_config.ini')

DEBUG = config['config']['debug']
HOST = config['config']['host']
PORT = config['config']['port']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', port = PORT, apps = jsonify(create_dictionary()))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/<plugin>/')
def plugins(plugin):
    main_page = confing[plugin]
    return 

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
