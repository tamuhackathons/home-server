from flask import Blueprint, redirect
from containers.docker_helper import *

docker_api = Blueprint('docker_api', __name__)

@docker_api.route('/add', methods=['POST'])
def add_app():
    app_name = request.form.get('name')
    url = request.form.get('url')
    status = 'SUCCESS' if create_new_plugin(url, app_name) == 200 else 'FAILED'
    
    redirect('/')
    
@docker_api.route('/start/<name>', methods=['POST'])
def start_con(name):
    start_container(name)
    
    return redirect('/')

@docker_api.route('/stop/<name>', methods=['POST'])
def stop_con(name):
    stop_container(name)
    
    return redirect('/')

@docker_api.route('/delete', methods=['DELETE'])
def delete_app():
    try:
        delete_container(request.form.get('name'))
    except:
        return jsonify({ 'status': 'FAILED' })
    
    return jsonify({ 'status': 'SUCCESS' })

@docker_api.route('/edit', methods=['POST'])
def edit_apps_post():
    try:
        rename_container(request.form.get('name'), request.form.get('new_name'))
    except:
        return jsonify({'status': 'FAILED'})
    
    return jsonify({'status': 'SUCCESS'})
