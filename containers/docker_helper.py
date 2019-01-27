import docker, configparser, socket, sys
sys.path.append('.')
from plugins.plugin_parser import add_plugin, remove_plugin

client = docker.from_env()


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    
    return port

def get_container_by_name(name):
    for container in get_all_containers():
        if container.name == name:
            return container

def current_running_containers():
    return client.containers(filters={'status': 'running'})

def current_stopped_containers():
    return client.containers(filters={'status': 'exited'})

def get_all_containers():
    return client.containers()

def create_new_plugin(docker_url, name):
    try:
        bind_port = get_free_tcp_port()
        client.containers.run(docker_url, name=name, ports={'80/tcp':str(bind_port)}, detach=True)
        add_plugin(name, name, f'localhost:{bind_port}')
        return 200
    except docker.errors.ContainerError as e:
        print(e)
    except docker.errors.ImageNotFound as e:
        print(e)
    except docker.errors.APIError as e:
        print(e)
        
    return 400
    
def stop_container(name):
    container = get_container_by_name(name)
    container.stop()
        
def start_container(name):
    container = get_container_by_name(name)
    container.start()
    
def get_container_names(containers):
    names = None
    
    for container in containers:
        names.append(container.name)
        
    return names

def delete_container(name):
    container = get_container_by_name(name)
    stop_container(container)
    container.remove()
    remove_plugin(name)
            
def rename_container(old_name, new_name):
    container = get_container_by_name(old_name)
    stop_container(container)
    container.rename(new_name)
    
if __name__ == '__main__':
    print(current_running_containers())
