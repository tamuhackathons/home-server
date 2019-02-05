from flask import Blueprint, jsonify
from sysinfo.sys_info import *

system_api = Blueprint('system_api', __name__)

@system_api.route('/cpu')
def get_cpu_inf():
    return jsonify(cpu_info())

@system_api.route('/memory')
def get_mem_inf():
    return jsonify(memory_info())

@system_api.route('/disk')
def get_dsk_inf():
    return jsonify(disk_info())

@system_api.route('/network')
def get_net_inf():
    return jsonify(network_info())

@system_api.route('/sensor')
def get_sen_inf():
    return jsonify(sensor_info())

@system_api.route('/user')
def get_usr_inf():
    return jsonify(user_info())

@system_api.route('/sys')
def get_all_sys():
    return jsonify(return_all_info())
