import configparser, socket

config = configparser.ConfigParser()

def url_exists(url):
    try:
        socket.gethostbyname(url)
        return True
    except socket.gaierror as e:
        return False

def create_dictionary():
    config.read('plugins/plugins_config.ini')
    plugins = {}
    for plugin in config.sections():
        plugins[plugin] = {}
        for info in config.options(plugin):
            plugins[plugin][info] = config.get(plugin, info)
    
    return plugins

def write_config():
    with open('plugins/plugins_config.ini', 'w') as config_file:
        config.write(config_file)

def add_plugin(plugin_name, url):
    config.read('plugins/plugins_config.ini')
    config.add_section(plugin_name)
    config.set(plugin_name, "name", plugin_name)
    if url.startswith('http'):
        config.set(plugin_name, "url", url)
    else:
        config.set(plugin_name, "url", f'http://{url}')
    write_config()
        
def remove_plugin(plugin_name):
    config.read('plugins/plugins_config.ini')
    config.remove_section(plugin_name)
    
    write_config()

def edit_plugin(plugin_name, new_name):
    config.read('plugins/plugins_config.ini')
    try:
        url = config[plugin_name]['url']
        
        remove_plugin(plugin_name)
        add_plugin(new_name, url)
        write_config()
    except:
        pass
    
def accessable_plugins():
    config.read('plugins/plugins_config.ini')
    plugins = {}
    
    for plugin in config.sections():
        if ('http://localhost' or 'https://localhost') not in config[plugin]['url']:
            plugins[plugin] = {'is_accessable': url_exists(config[plugin]['url'])}
    
    return plugins

if __name__ == '__main__':
    print(accessable_plugins())
