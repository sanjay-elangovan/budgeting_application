import pandas as pd
from config.fields import Fields as F
from config.files import Files
from file_handler.config_handler import read_config
from file_handler.data_handler import read_generated_data, save_generated_file
from constants import TRANSACTIONS, GENERATED_FILE

AGGREGATE_FIELDS = [
    F.transaction_key,
    F.amount,
    F.transaction_category,
    F.date,
]

class AnalyzeData:
    def make_calculations(self):
        # Read in the config and current transactions
        generated_file_config = read_config(GENERATED_FILE)
        classified_transactions = read_generated_data(generated_file_config, Files.classified_transactions)

        # Run analysis pipeline
        aggregated_data = (
            classified_transactions
            .pipe(self._aggregate_data)
            .pipe(self._select_fields)
        )

        # Output Analysis Files
        save_generated_file(aggregated_data, generated_file_config, Files.aggregated_transactions)

    @staticmethod
    def _aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
        df[F.amount] = df[F.amount].astype(float)
        return (
            df
            .groupby(F.transaction_key)[[F.amount]].sum()
            .merge(df, on=F.transaction_key, suffixes=(None, "_to_drop"))
            .sort_values(by=F.transaction_category)
            .drop_duplicates([F.transaction_key, F.amount], keep="first")
        )

    @staticmethod
    def _select_fields(df: pd.DataFrame) -> pd.DataFrame:
        return df[AGGREGATE_FIELDS].sort_values(by=F.transaction_key)