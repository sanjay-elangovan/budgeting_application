import pandas as pd
from config.fields import Fields as F
import shutil
import os


def get_date(transactions: pd.DataFrame) -> str:
    date_string = transactions[F.date].dt.strftime("%m%y").iloc[0]
    return date_string


def get_archive_filename(transactions: pd.DataFrame, file: str, file_type: str) -> str:
    date_string = get_date(transactions)
    return date_string + "_" + file + "." + file_type


def get_current_filename (file: str, file_type: str) -> str:
    return file + "." + file_type


def archive_file(transactions: pd.DataFrame, config: dict, config_name: str) -> None:
    archive_path = os.path.join(config[F.archive_path], get_archive_filename(transactions, config_name, config[F.extension]))
    shutil.copy(config[F.path], archive_path)


def save_generated_file(df: pd.DataFrame, config: dict, file: str) -> None:
    generated_file_config = config[file]
    df.to_csv(os.path.join(generated_file_config[F.path], get_current_filename(file, generated_file_config[F.extension])))
    df.to_csv(os.path.join(generated_file_config[F.archive_path],  get_archive_filename(df, file, generated_file_config[F.extension])))


def read_raw_data(config: dict) -> pd.DataFrame:
    return pd.read_csv(config[F.path], skiprows=config[F.skiprows])

def read_generated_data(config: dict, file: str) -> pd.DataFrame:
    file_config = config[file]
    generated_data_filepath = os.path.join(file_config[F.path], (file + "." + file_config[F.extension]))
    return pd.read_csv(generated_data_filepath)
