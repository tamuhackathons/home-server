import docker

client = docker.from_env()

def current_running_containers():
    return client.containers.list(filters={'status': 'running'})

def create_new_plugin(docker_url, name):
    pass

if __name__ == '__main__':
    print(current_running_containers())
