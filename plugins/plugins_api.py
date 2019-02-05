from flask import Blueprint
from plugins.plugin_parser import *

plugin_api = Blueprint('plugin_api', __name__)

@plugin_api.route('/add', methods=['POST'])
def add_app():
    app_name = request.form.get('name')
    url = request.form.get('url')

    add_plugin(app_name, url)

    return redirect('/')

@plugin_api.route('/edit', methods=['POST'])
def edit_apps_post():
    print('Editing', request.form.get('url'))
    try:
        edit_plugin(request.form.get('name'), request.form.get('new_name'))
        return jsonify({ 'status': 'SUCCESS'})
    except:
        return jsonify({ 'status': 'FAILED' })
    
@plugin_api.route('/delete', methods=['DELETE'])
def delete_app():
    try:
        remove_plugin(request.form.get('name'))
        return jsonify({ 'status': 'SUCCESS'})
    except:
        return jsonify({ 'status': 'FAILED' })
