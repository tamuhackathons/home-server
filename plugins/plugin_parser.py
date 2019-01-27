import configparser, socket

config = configparser.ConfigParser()
config.read('plugins/plugins_config.ini')

def url_exists(url):
    try:
        socket.gethostbyname(url)
        return True
    except socket.gaierror as e:
        return False

def create_dictionary():
    plugins = {}
    for plugin in config.sections():
        plugins[plugin] = {}
        for info in config.options(plugin):
            plugins[plugin][info] = config.get(plugin, info)
    
    return plugins

def add_plugin(plugin_name, url):
    config.add_section(plugin_name)
    config.set(plugin_name, "name", plugin_name)
    config.set(plugin_name, "url", url)
    
    with open('plugins/plugins_config.ini', 'w') as config_file:
        config.write(config_file)
        
def remove_plugin(plugin_name):
    config.remove_section(plugin_name)
    
    with open('plugins/plugins_config.ini', 'w') as config_file:
        config.write(config_file)

def edit_plugin(plugin_name, new_name):
    try:
        url = config[plugin_name]['url']
        
        remove_plugin(plugin_name)
        add_plugin(new_name, url)
    except:
        pass
    
def accessable_plugins():
    plugins = {}
    
    for plugin in config.sections():
        if ('http://localhost' or 'https://localhost') not in config[plugin]['url']:
            plugins[plugin] = {'is_accessable': url_exists('config[plugin]['url']')}
    
    return plugins

if __name__ == '__main__':
    print(accessable_plugins())
