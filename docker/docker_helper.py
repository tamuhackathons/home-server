import docker

client = docker.from_env()

def current_running_containers():
    return client.containers.list(filters={'status': 'running'})

if __name__ == '__main__':
    print(current_running_containers())
