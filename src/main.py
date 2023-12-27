import pandas as pd
import taipy as tp
from taipy.gui import Gui, Icon, navigate
from config.config import scenario_cfg
from taipy.config import Config 
from pages.main_dialog import *

import warnings
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

# Load configuration
Config.load('config/config.toml')
scenario_cfg = Config.scenarios['supplychain_predict']

# Execute the scenario
tp.Core().run()

def create_first_scenario(scenario_cfg):
    """Create and submit the first scenario."""
    scenario = tp.create_scenario(scenario_cfg)
    tp.submit(scenario)
    return scenario

scenario = create_first_scenario(scenario_cfg)

# Read datasets
train_dataset = scenario.train_dataset.read()


# # Prepare data for visualization
# select_x = test_dataset.drop('EXITED',axis=1).columns.tolist()
# x_selected = select_x[0]
# select_y = select_x
# y_selected = select_y[1]

# # Read results and create charts
# values = scenario.results_ml.read()
# forecast_series = values['Forecast']
# scatter_dataset_pred = creation_scatter_dataset_pred(test_dataset, forecast_series)
# histo_full_pred = creation_histo_full_pred(test_dataset, forecast_series)
# histo_full = creation_histo_full(test_dataset)



def on_change(state, var_name, var_value):
    """Handle variable changes in the GUI."""
    if var_name in ['x_selected', 'y_selected']:
        update_histogram_and_scatter(state)
    elif var_name == 'db_table_selected':
        handle_temp_csv_path(state)

# GUI initialization
menu_lov = [
    ("Data Visualization", Icon('images/histogram_menu.svg', 'Data Visualization')),
    ('Databases', Icon('images/Datanode.svg', 'Databases'))
]

root_md = """
<|toggle|theme|>
<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>
"""

page = "Data Visualization"

def menu_fct(state, var_name, var_value):
    """Function that is called when there is a change in the menu control."""
    state.page = var_value['args'][0]
    navigate(state, state.page.replace(" ", "-"))


def on_init(state):
    update_histogram_and_scatter(state)

# Define pages
pages = {
    "/": root_md + dialog_md,
    "Data-Visualization": dv_data_visualization_md,
    "Databases": db_databases_md,
}

# Run the GUI
if __name__ == '__main__':
    gui = Gui(pages=pages)
    gui.run(title="Supply Chain Prediction", dark_mode=False, port=8494)
