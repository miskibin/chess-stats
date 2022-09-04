import os
import yaml
import logging.config
import logging
import coloredlogs

def get_logger(config_path = r'src\common\logging.yaml', default_level=logging.DEBUG):
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')
    return logging.getLogger()


