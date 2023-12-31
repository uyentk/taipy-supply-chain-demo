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
preprocessed_dataset = scenario.preprocessed_dataset.read()

# Prepare data for visualization
select_prod = list(result_dataset['product name'].unique()) 
prod_selected = select_prod[0]

select_state = list(initial_dataset['Customer State'].unique()) 
cus_state_selected = select_state[0]

# Create charts
forecast_series = result_dataset['y']
line_dataset = creation_line_dataset(result_dataset, prod_selected)
map_dataset_displayed = creation_map_dataset(initial_dataset, prod_selected)
rmse, mape, mae = metrics_calculation(result_dataset, prod_selected)
line_sales_dataset = creation_line_sales(preprocessed_dataset, prod_selected)
hist_dataset = creation_hist_dataset(initial_dataset, prod_selected)
state_dataset = top_N_prod_by_state(initial_dataset, cus_state_selected)
order_quantity_dataset = order_quantity_by_state(initial_dataset, cus_state_selected)

print(order_quantity_dataset)
print(order_quantity_dataset.columns)

def on_change(state, var_name, var_value):
    """Handle variable changes in the GUI."""
    if var_name == 'prod_selected':
        update_variables_product(state, var_value)
        update_viz(state)
        update_map(state)
    elif var_name == 'cus_state_selected':
        update_charts_cus_state(state, var_value)
        update_hist_state(state)
    elif var_name == 'db_table_selected':
        handle_temp_csv_path(state)

# GUI initialization
menu_lov = [
    ("Model Management", Icon('images/compare.svg', 'Model Management')),
    ('Databases', Icon('images/Datanode.svg', 'Databases')),
    ('Data Visualization', Icon('images/histogram_menu.svg', 'Data Visualization'))
]

root_md = """
<|toggle|theme|>
<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>
"""

page = "Model Management"

def menu_fct(state, var_name, var_value):
    """Function that is called when there is a change in the menu control."""
    state.page = var_value['args'][0]
    navigate(state, state.page.replace(" ", "-"))

def update_variables_product(state, product):
    """Update the different variables and dataframes used in the application."""
    state.prod_selected = product
    update_charts_product(state, product)

def update_variables_state(state, cus_state):
    state.cus_state_selected = cus_state
    update_charts_cus_state(state, cus_state)

def update_charts_product(state, product):
    """This function updates all the charts of the GUI."""
    state.line_dataset = creation_line_dataset(result_dataset, product)
    state.map_dataset_displayed = creation_map_dataset(initial_dataset, product)
    state.rmse, state.mape, state.mae = metrics_calculation(result_dataset, product)
    state.line_sales_dataset = creation_line_sales(preprocessed_dataset, product)
    state.hist_dataset = creation_hist_dataset(initial_dataset, product)

def update_charts_cus_state(state, cus_state):
    state.state_dataset = top_N_prod_by_state(initial_dataset, cus_state)
    state.order_quantity_dataset = order_quantity_by_state(initial_dataset, cus_state)

def on_init(state):
    update_viz(state)
    update_map(state)
    update_hist_state(state)

# Define pages
pages = {
    "/": root_md, #+ dialog_md,
    "Model-Management": dv_model_management_md,
    "Databases": db_databases_md,
    "Data-Visualization": dv_data_visualization_md,
}

stylekit = {
  "color_primary": "#BADA55",
  "color_secondary": "#FF5733",
}

# Run the GUI
if __name__ == '__main__':
    gui = Gui(pages=pages)
    gui.run(title="Supply Chain Prediction", dark_mode=False, port=8494, use_reloader= True, stylekit= stylekit)
