import docker, configparser, socket, sys
sys.path.append('.')
from plugins.plugin_parser import add_plugin, remove_plugin, edit_plugin

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
        
def get_container_image(name):
    for container in get_all_containers():
        if container.name == name:
            return container.image.short_id[7:]

def current_running_containers():
    return client.containers.list(filters={'status': 'running'})

def current_stopped_containers():
    return client.containers.list(filters={'status': 'exited'})

def get_all_containers():
    return client.containers.list(all=True)

def create_new_plugin(docker_url, name):
    try:
        bind_port = get_free_tcp_port()
        client.containers.run(docker_url, name=name, ports={'80/tcp':str(bind_port)}, detach=True)
        add_plugin(name, f'localhost:{bind_port}')
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
    if ('exited' or 'restarting' or 'paused') not in container.status:
        container.stop()
        
def start_container(name):
    container = get_container_by_name(name)
    if 'running' not in container.status:
        container.start()
    
def get_container_names(containers):
    names = None
    
    for container in containers:
        names.append(container.name)
        
    return names

def delete_container(name):
    container = get_container_by_name(name)
    container.stop()
    container.remove()
    remove_plugin(name)
            
def rename_container(old_name, new_name):
    image = get_container_image(old_name)
    print(image)
    container = get_container_by_name(old_name)
    print(container)
    delete_container(old_name)
    print(new_name)
    create_new_plugin(image, new_name)

    
if __name__ == '__main__':
    print(current_running_containers())
