import pandas as pd

from config.files import Files
from config.fields import Fields as F
from file_handler.config_handler import read_config
from file_handler.data_handler import read_raw_data, archive_file, save_generated_file
from constants import FILES

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
        datasource_config = read_config(FILES)[F.datasources]
        generated_file_config = read_config(FILES)[F.generated_files]

        # Loop through datasources in config to read in each datasource. Combine into one dataframe.
        transactions = pd.DataFrame()
        for config_name in datasource_config:
            config = datasource_config[config_name]
            raw_data = read_raw_data(config)

            # Clean the raw data
            cleaned_data = (
                raw_data
                .pipe(self._unify_columns, config=config)
                .pipe(self._unify_transactions)
                .pipe(self._get_dates)
                .pipe(self._add_source, config_name=config_name)
                .pipe(self._clean_descriptions)
                .pipe(self._drop_invalid_amounts)
            )
            # Combine and reset the index
            transactions = pd.concat([transactions, cleaned_data])
            transactions.reset_index(inplace=True, drop=True)

            # Move parsed file into archive directory
            archive_file(transactions, config, config_name)

        # Save transactions to archive
        save_generated_file(transactions, generated_file_config, Files.transactions)

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
