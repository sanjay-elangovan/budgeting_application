import pandas as pd

from config.files import Files
from config.fields import Fields as F
from file_handler.config_handler import read_config
from file_handler.data_handler import get_archive_filename
from constants import DATASOURCES, TRANSACTIONS_FOLDER, TRANSACTIONS_ARCHIVE_FOLDER

AMOUNT_CLEANING = {
    ",": "",
    "\(\$": "-",
    "\)": "",
    "\$": "",
    "\+ ": "",
    "- ": "-"
}


class ReadData:
    def make_calculations(self) -> None:
        # Get Datasource and Configs
        datasources_config = read_config(DATASOURCES)

        # Loop through config to read in each datasource. Combine into one dataframe.
        transactions = pd.DataFrame()
        for config_name in datasources_config:
            config = datasources_config[config_name]
            raw_data = self._read_datasource(config)
            cleaned_data = (
                raw_data
                .pipe(self._unify_columns, config=config)
                .pipe(self._unify_transactions)
                .pipe(self._get_dates)
                .pipe(self._add_source, config_name=config_name)
                .pipe(self._clean_descriptions)
            )
            transactions = pd.concat([transactions, cleaned_data])
            transactions.reset_index(inplace=True, drop=True)

        # Pickle transactions and save to archive
        transactions.to_pickle(TRANSACTIONS_FOLDER / Files.current_transactions_pkl)
        transactions.to_csv(TRANSACTIONS_ARCHIVE_FOLDER / get_archive_filename(transactions, Files.current_transactions_pkl))

    @staticmethod
    def _read_datasource(config: dict) -> pd.DataFrame:
        return pd.read_csv(config[F.path], skiprows=config[F.skiprows])

    @staticmethod
    def _unify_columns(transactions: pd.DataFrame, config: dict) -> pd.DataFrame:
        return transactions.rename(columns=config[F.column_mapping])

    @staticmethod
    def _unify_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
        transactions[F.amount] = transactions[F.amount].replace(AMOUNT_CLEANING, regex=True).astype('float')
        return transactions

    @staticmethod
    def _get_dates(transactions: pd.DataFrame) -> pd.DataFrame:
        transactions[F.date] = pd.to_datetime(transactions[F.date])
        return transactions

    @staticmethod
    def _add_source(transactions: pd.DataFrame, config_name: str) -> pd.DataFrame:
        transactions[F.source] = config_name
        return transactions

    @staticmethod
    def _clean_descriptions(transactions: pd.DataFrame) -> pd.DataFrame:
        """
        Fill NaN description with 'No Information'
        Lowercase all descriptions
        Remove all spaces
        """
        transactions[F.cleaned_description] = (
            transactions[F.description]
            .fillna("No information")
            .str.lower()
            .str.replace('\W+', "", regex=True)
        )
        return transactions
