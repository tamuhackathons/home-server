from flask import Flask, render_template, jsonify, request, redirect
from plugins.plugin_parser import create_dictionary
from containers.docker_helper import current_running_containers
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

@app.route('/addplugin', methods=['GET'])
def plugin_page():
    return render_template('add_app.html', port = PORT) 

@app.route('/addplugin', methods=['POST'])
def add_app():
    app_name = request.form.get('name')
    docker_url = request.form.get('docker_url')

    status = None
    return redirect('/addpluginstatus/{}'.format(status))

@app.route('/addpluginstatus/<status>')
def add_app_status(status):
    return render_template('add_app_result.html', port = PORT, status = status)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
