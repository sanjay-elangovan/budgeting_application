class Fields:
    # Raw data fields
    posted_date = "Posted Date"
    payee = "Payee"
    datetime = "Datetime"
    note = "Note"
    amount_total = "Amount(total)"

    # Cleaned data fields
    amount = "Amount"
    date = "Date"
    description = "Description"

    # Generated fields
    source = "source"
    cleaned_description = "cleaned_description"
    transaction_key = "transaction_key"
    transaction_category = "transaction_category"

    # Config fields
    datasources = "datasources"
    generated_files = "generated_files"
    path = "path"
    archive_path = "archive_path"
    skiprows = "skiprows"
    extension = "extension"
    column_mapping = "column_mapping"
    known_values = "known_values"
    config_description = "description"