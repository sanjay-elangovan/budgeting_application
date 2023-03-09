from pathlib import Path

ROOT_FOLDER = Path(__file__).parent.parent
BUDGETING_APPLICATION = ROOT_FOLDER / "budgeting_application"

CONFIG_FOLDER = BUDGETING_APPLICATION / "config"
FILES_CONFIG = CONFIG_FOLDER / "files_config.yaml"
TRANSACTIONS_CONFIG = CONFIG_FOLDER / "transactions_config.yaml"

FILES = "files"
TRANSACTIONS = "transactions"
