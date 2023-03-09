import pandas as pd
from tabulate import tabulate
import re

from config.files import Files
from config.fields import Fields as F
from file_handler.config_handler import read_config, write_config
from constants import TRANSACTIONS, TRANSACTIONS_FOLDER, TRANSACTIONS_ARCHIVE_FOLDER

SELECTED_COLUMNS = [
    F.date,
    F.description,
    F.amount,
    F.source,
    F.transaction_key,
    F.transaction_category
]


class ClassifyData:
    def make_calculations(self) -> None:
        # Read in the transactions config and current transactions
        config = read_config(TRANSACTIONS)
        current_transactions = pd.read_pickle(TRANSACTIONS_FOLDER / Files.current_transactions_pkl)

        # Run classification pipeline - Automatically identify transactions, then ask the user to identify the rest
        classified_data = (
            current_transactions.pipe(self._identify_known_transactions, config=config)
            .pipe(self._select_columns)
            .pipe(self._identify_unknown_transactions, config=config)
        )

        # Save off data for manual review
        classified_data.to_csv(TRANSACTIONS_FOLDER / Files.classified_current_transactions_csv)

        # Read in files after manual review, save into archive
        reviewed_data = pd.read_csv(TRANSACTIONS_FOLDER / Files.classified_current_transactions_csv)
        reviewed_data.to_csv(TRANSACTIONS_ARCHIVE_FOLDER / self.get_archive_filename(reviewed_data, Files.classified_current_transactions_csv))


    @staticmethod
    def _identify_known_transactions(df: pd.DataFrame, config: dict) -> pd.DataFrame:
        for key in config:
            # Join together the known values into a string. This string will be regex matched against.
            known_values_string = ("|").join(config[key][F.known_values])
            description = config[key][F.config_description]

            # If the known_values string isn't empty, create a new column called "transaction_type" with the type
            if len(known_values_string) > 1:
                df.loc[df[F.cleaned_description].str.contains(known_values_string), [F.transaction_key,
                                                                                     F.transaction_category]] = key, description

        return df

    @staticmethod
    def _identify_unknown_transactions(df: pd.DataFrame, config: dict) -> pd.DataFrame:
        # Filter to unknown transactions
        unknown_transactions = df.query("transaction_key.isnull()").reset_index()

        # Format the transactions and config for printing
        printable_df = unknown_transactions.loc[:,
                       ~unknown_transactions.columns.isin([F.transaction_key, F.transaction_category])]
        config_df = pd.DataFrame(config).drop(labels="known_values")

        # Go through each of the unknown transactions and give them categories
        manually_labeled_transactions = unknown_transactions[['index']]
        typelist = []
        for i in manually_labeled_transactions['index']:
            print(tabulate(printable_df.query('index == ' + str(i)), headers='keys', tablefmt='fancy_grid'))
            print(tabulate(config_df, headers='keys', tablefmt='fancy_grid'))
            manual_transaction_key = int(input("Correct transaction key: "))
            typelist.append(manual_transaction_key)

            # Update known values based on new entry
            ClassifyData._update_known_values(config, manual_transaction_key)

        # Dump the new config file
        write_config(config, TRANSACTIONS)

        # Update the manual labels
        manually_labeled_transactions['transaction_key'] = typelist
        return df.combine_first(manually_labeled_transactions.set_index('index'))

    @staticmethod
    def _update_known_values(config: dict, manual_transaction_key: int) -> None:
        new_value = (
            re.sub('\W+', "", input("What can we add to the known transactions? Leave blank if none. ")
                   .lower()
                   )
        )

        if len(new_value) > 1:
            config[manual_transaction_key][F.known_values].append(new_value)

    @staticmethod
    def _select_columns(df: pd.DataFrame) -> pd.DataFrame:
        return df[SELECTED_COLUMNS]
