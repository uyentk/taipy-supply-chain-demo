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
Config.load('config/config_supply.toml')
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
initial_dataset = scenario.initial_dataset.read()
# train_dataset = scenario.train_dataset.read()
result_dataset = scenario.trained_infer.read()

# Prepare data for visualization
select_prod = list(result_dataset['product name'].unique())
prod_selected = select_prod[0]

# Create charts
forecast_series = result_dataset['y']
line_dataset = creation_line_dataset(result_dataset, prod_selected)

def on_change(state, var_name, var_value):
    """Handle variable changes in the GUI."""
    if var_name == 'prod_selected':
        update_variables(state, var_value)
        update_viz(state)
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

def update_variables(state, product):
    """Update the different variables and dataframes used in the application."""
    # global scenario
    state.prod_selected = product
    
    update_charts(state, product)

def update_charts(state, product):
    """This function updates all the charts of the GUI."""
    state.line_dataset = creation_line_dataset(result_dataset, product)


def on_init(state):
    update_viz(state)

# Define pages
pages = {
    "/": root_md, #+ dialog_md,
    "Data-Visualization": dv_data_visualization_md,
    "Databases": db_databases_md,
}

# Run the GUI
if __name__ == '__main__':
    gui = Gui(pages=pages)
    gui.run(title="Supply Chain Prediction", dark_mode=False, port=8494, use_reloader= True)
