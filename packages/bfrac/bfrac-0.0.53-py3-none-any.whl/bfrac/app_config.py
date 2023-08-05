import os
import json
import configparser


class AppConfig:
    """
    Reads config.ini file and provides access assets such as
    the api key, path to data dragon directory, and other assets.
    """
    def __init__(self, in_config_file_path="config.ini"):
        print(f"Config : {os.path.abspath(in_config_file_path)}")
        # Read config file to get data locations.
        config = configparser.ConfigParser()
        config.read(in_config_file_path)
        self._root_dir = config['DEFAULT']['root_dir']
        riot_api_key_file_rel = config['DEFAULT']['riot_api_key_file_rel']
        self._data_dragon_dir = os.path.join(self._root_dir, config['DEFAULT']['data_dragon_dir_rel'])
        self._data_dragon_sub_dir = self._data_dragon_dir
        # Load RiotAPI key from file.
        with open(os.path.join(self._root_dir, riot_api_key_file_rel)) as f:
            self._API_KEY = json.loads(f.read())["API_KEY"]

    def get_key(self):
        """Get the Riot API key"""
        return self._API_KEY

    def get_root_dir(self):
        """Get the path to root directory for all assets"""
        return self._root_dir

    def get_dragon_dir(self):
        """Get the path to root directory of the data dragon"""
        return self._data_dragon_dir
