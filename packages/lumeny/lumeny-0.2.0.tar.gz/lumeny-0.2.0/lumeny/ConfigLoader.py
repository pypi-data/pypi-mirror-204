import yaml
import os
from typing import Any

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "lumeny")

def load_config(config_dir:str = CONFIG_DIR) -> Any:
    with open(os.path.join(config_dir, "config.yml"), "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

class ConfigLoader:
    def __init__(self, config_dir:str = CONFIG_DIR) -> None:
        self.config_dir = config_dir
        self.config = load_config(config_dir)
        self.init_config()
    
    def get_config(self) -> Any:
        return self.config
    
    # initialize config file with following sections: miniflux, caldav, and openai
    def init_config(self) -> None:
        # if the section exists, preserve the content
        # if the section does not exist, create it
        config = self.get_config()
        if "miniflux" not in config.keys():
            config["miniflux"] = {}
        if "caldav" not in config.keys():
            config["caldav"] = {}
        if "openai" not in config.keys():
            config["openai"] = {}
        self.write_config(config)
    
    def write_config(self, config:Any) -> None:
        with open(os.path.join(self.config_dir, "config.yml"), "w") as config_file:
            yaml.safe_dump(config, config_file)
    
    ## add to config specific section
    def add_to_config(self, section:str, key:str, value:Any) -> None:
        config = self.get_config()
        config[section][key] = value
        self.write_config(config)
    
def main():
    config_loader = ConfigLoader()

if __name__ == "__main__":
    main()