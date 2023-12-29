import pathlib

# This path is used to create a temporary CSV file download the table
tempdir = pathlib.Path(".tmp")
tempdir.mkdir(exist_ok=True)
PATH_TO_TABLE = str(tempdir / "table.csv")

# Selector to select the table to show
db_table_selector = ['Training Dataset', 'Result Table']
db_table_selected = db_table_selector[0]

def handle_temp_csv_path(state):
    """This function checks if the temporary csv file exists. If it does, it is deleted. Then, the temporary csv file
    is created for the right table

    Args:
        state: object containing all the variables used in the GUI
    """
    if state.db_table_selected == "Training Dataset":
        state.initial_dataset.to_csv(PATH_TO_TABLE, sep=';')
    if state.db_table_selected == "Result Table":
        state.result_dataset.to_csv(PATH_TO_TABLE, sep=';')


# Aggregation of the strings to create the complete page
db_databases_md = """
# Data**bases**{: .color-primary}

<|layout|columns=1 1|
<|{db_table_selected}|selector|lov={db_table_selector}|dropdown|label=Table|>

<|{PATH_TO_TABLE}|file_download|name=table.csv|label=Download table|>
|>

<Training|part|render={db_table_selected=='Training Dataset'}|
<|{initial_dataset}|table|>
|Training>

<Result|part|render={db_table_selected=='Result Table'}|
<|{result_dataset}|table|>
|Result>
""" 

