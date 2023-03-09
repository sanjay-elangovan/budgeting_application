import pandas as pd
import yaml
from constants import DATASOURCES_CONFIG, TRANSACTIONS_CONFIG, DATASOURCES, TRANSACTIONS


def read_config(config_selection: str) -> dict:
    config_path = config_selector(config_selection)
    return config_yaml_reader(config_path)

def write_config(updated_yaml: dict, config_selection: str) -> dict:
    config_path = config_selector(config_selection)
    return config_yaml_writer(updated_yaml, config_path)

def config_yaml_writer(updated_yaml: dict, config_path: str) -> None:
    with open(config_path, 'w') as outfile:
        yaml.dump(updated_yaml, outfile, default_flow_style=False)

def config_yaml_reader(config_path: str) -> dict:
    """
    Read in config from config path.
    """
    with open(config_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return config


def config_selector(config_selection: str) -> str:
    if config_selection == DATASOURCES:
        config_path = DATASOURCES_CONFIG
    elif config_selection == TRANSACTIONS:
        config_path = TRANSACTIONS_CONFIG

    return config_path
