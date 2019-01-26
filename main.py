from flask import Flask, render_template, jsonify
from plugins.plugin_parser import create_dictionary
from docker.docker_helper import current_running_containers
import configparser

config = configparser.ConfigParser()
config.read('main_config.ini')

DEBUG = config['config']['debug']
HOST = config['config']['host']
PORT = config['config']['port']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', port = PORT, apps = create_dictionary())

@app.route('/home')
def home():
    return render_template('home.html', containers = current_running_containers())

@app.route('/<plugin>/')
def plugins(plugin):
    main_page = config[plugin]
    return 

@app.route('/addplugin', methods=['POST'])
def add_app():
    
    return 

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
