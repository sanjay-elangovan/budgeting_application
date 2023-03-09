from pathlib import Path

ROOT_FOLDER = Path(__file__).parent.parent
BUDGETING_APPLICATION = ROOT_FOLDER / "budgeting_application"

CONFIG_FOLDER = BUDGETING_APPLICATION / "config"
DATASOURCES_CONFIG = CONFIG_FOLDER / "datasources_config.yaml"
TRANSACTIONS_CONFIG = CONFIG_FOLDER / "transactions_config.yaml"

TRANSACTIONS_FOLDER = ROOT_FOLDER / "transactions"
TRANSACTIONS_ARCHIVE_FOLDER = TRANSACTIONS_FOLDER / "archived_transactions"

DATASOURCES = "datasources"
TRANSACTIONS = "transactions"
