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

if __name__ == '__main__':
    print(create_dictionary())
