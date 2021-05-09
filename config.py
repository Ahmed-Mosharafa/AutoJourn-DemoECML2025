"""
   Read configuration parameters from configuration file
"""

import json
import os


class Config:
    # General config (default value is empty)
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""


config_vars = {config: t for config, t in vars(Config).items() if not config.startswith('__')}


def _read_config(source):
    """
        Read configuration from source into a dictionary
    """
    result = {}
    for config, default in config_vars.items():
        t = type(default)
        if config in source:
            result[config] = t(source[config])
    return result


def _get_file_config(testing=False):

    """
        Read configuration from file
    """

    file_name = 'config.json'
    file_path = 'TextSummarizationLab21/' + file_name

    with open(file_path) as f:
        file_config = json.load(f)
        return _read_config(file_config)


def _get_env_config():
    """
        Read configuration from defined env variables
    """
    return _read_config(os.environ)


def _get_config(config, *stages):
    for stage in stages:  # return the value of the first stage defining the value
        if config in stage:
            return stage[config]


def init():
    file_config = _get_file_config()  # read configuration from file
    env_config = _get_env_config()  # read configurations from environment (env variables)

    # Define configurations as stages in the order of most priority (e.g., env variables has top priority)
    stages = env_config, file_config

    # for each configuration variable get its value from first stage defining it.
    for config in config_vars:
        val = _get_config(config, *stages)
        if val is not None:
            setattr(Config, config, val)
        else:
            raise ValueError('Missing config \'{}\''.format(config))