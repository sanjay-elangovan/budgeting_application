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
                .pipe(self._drop_invalid_amounts)
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
    def _unify_columns(df: pd.DataFrame, config: dict) -> pd.DataFrame:
        return df.rename(columns=config[F.column_mapping])

    @staticmethod
    def _unify_transactions(df: pd.DataFrame) -> pd.DataFrame:
        df[F.amount] = df[F.amount].replace(AMOUNT_CLEANING, regex=True).astype('float')
        return df

    @staticmethod
    def _get_dates(df: pd.DataFrame) -> pd.DataFrame:
        df[F.date] = pd.to_datetime(df[F.date])
        return df

    @staticmethod
    def _add_source(df: pd.DataFrame, config_name: str) -> pd.DataFrame:
        df[F.source] = config_name
        return df

    @staticmethod
    def _clean_descriptions(df: pd.DataFrame) -> pd.DataFrame:
        """
        Fill NaN description with 'No Information'
        Lowercase all descriptions
        Remove all spaces
        """
        df[F.cleaned_description] = (
            df[F.description]
            .fillna("No information")
            .str.lower()
            .str.replace('\W+', "", regex=True)
        )
        return df

    @staticmethod
    def _drop_invalid_amounts(df: pd.DataFrame) -> pd.DataFrame:
        """
        Any amount which is null should be dropped - These had no effect on the budget
        """
        return df.dropna(subset=F.amount)
