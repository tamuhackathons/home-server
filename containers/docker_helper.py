import docker, configparser, socket, sys, ast
sys.path.append('.')
from plugins.plugin_parser import remove_plugin, edit_plugin

client = docker.from_env()

def write_config(config):
    with open('containers/docker_config.ini', 'w') as config_file:
        config.write(config_file)


def add_container(image, plugin_name, url, ports = {}, volumes = []):
    config = configparser.ConfigParser()
    config.read('containers/docker_config.ini')
    section_name = f'Docker-{image}-{plugin_name}'
    config.add_section(section_name)
    
    config.set(section_name, "name", plugin_name)
    config.set(section_name, "ports", str(ports))
    config.set(section_name, "volumes", str(volumes))
    config.set(section_name, "url", url)
    
    write_config(config)
    
def remove_container(image):
    config = configparser.ConfigParser()
    config.read('containers/docker_config.ini')
    config.remove_section(image)
    
    write_config(config)
    
def create_container_dictionary():
    config = configparser.ConfigParser()
    config.read('containers/docker_config.ini')
    containers = {}
    
    for container in config.sections():
        containers[container] = {}
        for data in config.options(container):
            containers[container][data] = config.get(container, data)
            
    return containers

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

def create_new_plugin(docker_url, name, port='80/tcp', ports=['80/tcp'], volumes=None):
    try:
        ports = ast.literal_eval(ports)
        volumes = ast.literal_eval(volumes)
        port_dict = {}
        for p in ports:
            port_dict[p] = str(get_free_tcp_port())
            
        client.containers.run(docker_url, name=name, ports=port_dict, volumes=volumes, detach=True)
        add_container(docker_url, name, f'http://localhost:{port_dict[port]}', port_dict, volumes)
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
    container = get_container_by_name(old_name)
    delete_container(old_name)
    create_new_plugin(image, new_name)

    
if __name__ == '__main__':
    print(current_running_containers())
