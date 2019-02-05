from flask import Flask, render_template, jsonify, request, redirect
from plugins.plugins_api import plugin_api
from sysinfo.system_api import system_api
from containers.docker_api import docker_api
from containers.docker_helper import get_all_containers
from plugins.plugin_parser import create_dictionary
import configparser, time

config = configparser.ConfigParser()
config.read('main_config.ini')

DEBUG = config['config']['debug']
HOST = config['config']['host']
PORT = config['config']['port']

app = Flask(__name__)
app.register_blueprint(system_api, url_prefix='/system')
app.register_blueprint(docker_api, url_prefix='/docker')
app.register_blueprint(plugin_api, url_prefix='/plugins')

@app.route('/')
def index():
    return render_template('index.html', port = PORT, apps = create_dictionary())

@app.route('/home')
def home():
    return render_template('home.html', port = PORT, containers = get_all_containers())

@app.route('/addplugin', methods=['GET'])
def plugin_page():
    return render_template('add_app.html', port = PORT) 


@app.route('/addpluginstatus/<status>')
def add_app_status(status):
    return render_template('add_app_result.html', port = PORT, status = status)

@app.route('/editapps')
def edit_apps_get():
    return render_template('edit_apps.html', port = PORT, apps = create_dictionary())


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
