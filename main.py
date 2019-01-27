from flask import Flask, render_template, jsonify, request, redirect
from plugins.plugin_parser import *
from containers.docker_helper import *
from sysinfo.sys_info import *
import configparser, time

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
    return render_template('home.html', port = PORT, containers = get_all_containers())

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
    
@app.route('/start/<name>', methods=['POST'])
def start_con(name):
    start_container(name)
    
    return redirect('/')

@app.route('/stop/<name>', methods=['POST'])
def stop_con(name):
    stop_container(name)
    
    return redirect('/')

@app.route('/cpu')
def get_cpu_inf():
    return jsonify(cpu_info())

@app.route('/memory')
def get_mem_inf():
    return jsonify(memory_info())

@app.route('/disk')
def get_dsk_inf():
    return jsonify(disk_info())

@app.route('/network')
def get_net_inf():
    return jsonify(network_info())

@app.route('/sensor')
def get_sen_inf():
    return jsonify(sensor_info())

@app.route('/user')
def get_usr_inf():
    return jsonify(user_info())

@app.route('/sys')
def get_all_sys():
    return jsonify(return_all_info())

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
