import docker, configparser
from plugins.plugin_parser import add_plugin

client = docker.from_env()

def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    
    return port

def current_running_containers():
    return client.containers.list(filters={'status': 'running'})

def current_stopped_containers():
    return client.containers.list(filers={'status': 'exited'})

def create_new_plugin(docker_url, name):
    try:
        bind_port = get_free_tcp_port
        client.containers.run(docker_url, name=name, ports={'80/tcp':str(bind_port)}, detach=True)
        add_plugin(name, name, f'localhost:{bind_port}')
        return 200
    except:
        return 400
    
def stop_container(name):
    for container in current_running_containers():
        if container.name == name:
            container.stop()
            break
        
def start_container(name):
    for container in current_stopped_containers():
        if container.name == name:
            container.start()
    

if __name__ == '__main__':
    print(current_running_containers())
