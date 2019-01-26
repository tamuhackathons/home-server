import configparser

config = configparser.ConfigParser()
config.read('plugins/plugins_config.ini')

def create_dictionary():
    plugins = {}
    for plugin in config.sections():
        plugins[plugin] = {}
        for info in config.options(plugin):
            plugins[plugin][info] = config.get(plugin, info)
    
    return plugins

def add_plugin(plugin_name, name, url):
    config.add_section(plugin_name)
    config.set(plugin_name, "name", name)
    config.set(plugin_name, "url", url)
    
    with open('plugins/plugins_config.ini', 'w') as config_file:
        config.write(config_file)
        
def remove_plugin(plugin_name):
    pass

if __name__ == '__main__':
    print(create_dictionary())
