from jproperties import Properties

configs = Properties()
with open('.properties', 'rb') as config_file:
    configs.load(config_file)


def get_property(key):
    """Gets a property from the config file."""
    return configs.get(key).data
