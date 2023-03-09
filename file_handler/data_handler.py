import pandas as pd
from config.fields import Fields as F
from config.files import Files


def get_archive_filename(transactions: pd.DataFrame, file: str) -> str:
    file_name = transactions[F.date].dt.strftime("%m%y").iloc[0] + "_" + file
    return file_name