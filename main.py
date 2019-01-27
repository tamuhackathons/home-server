from flask import Flask, render_template, jsonify, request, redirect
from plugins.plugin_parser import create_dictionary, add_plugin
from containers.docker_helper import current_running_containers, create_new_plugin, get_container_names
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
    return render_template('home.html', containers = get_container_names(current_running_containers()))

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
    url = request.form.get('url')
    checkbox = request.form.get('url_option')

    status = 'SUCCESS'

    if(checkbox == 'on'):
        # Docker
        status = 'SUCCESS' if create_new_plugin(url, app_name) == 200 else 'FAILED'
    elif(checkbox == 'off'):
        # URL
        add_plugin(app_name, url)

    return redirect('/')

@app.route('/addpluginstatus/<status>')
def add_app_status(status):
    return render_template('add_app_result.html', port = PORT, status = status)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
