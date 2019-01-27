from flask import Flask, render_template, jsonify, request, redirect
from plugins.plugin_parser import create_dictionary, add_plugin, edit_plugin, remove_plugin
from containers.docker_helper import current_running_containers, create_new_plugin, get_container_names, rename_container, delete_container
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
    else:
        # URL
        add_plugin(app_name, url)

    return redirect('/')

@app.route('/addpluginstatus/<status>')
def add_app_status(status):
    return render_template('add_app_result.html', port = PORT, status = status)

@app.route('/editapps')
def edit_apps_get():
    return render_template('edit_apps.html', port = PORT, apps = create_dictionary())

@app.route('/editapps', methods=['POST'])
def edit_apps_post():
    print('Editing', request.form.get('url'))
    try:
        if(request.form.get('url').startswith('http')):
            edit_plugin(request.form.get('name'), request.form.get('new_name'))
        else:
            rename_container(request.form.get('name'), request.form.get('new_name'))
        return jsonify({ 'status': 'SUCCESS'})
    except:
        return jsonify({ 'status': 'FAILED' })

@app.route('/deleteapp', methods=['DELETE'])
def delete_app():
    try:
        if(request.form.get('url').startswith('http')):
            remove_plugin(request.form.get('name'))
        else:
            delete_container(request.form.get('name'))
        return jsonify({ 'status': 'SUCCESS'})
    except:
        return jsonify({ 'status': 'FAILED' })
    

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
