import pandas as pd
import numpy as np


dv_graph_selector = ['Line', 'Map']
dv_graph_selected = dv_graph_selector[0]

# # Histograms dialog
# properties_histo_full = {}
# properties_scatter_dataset = {}

def creation_line_dataset(train_ds: pd.DataFrame, prod: str):
    line_dataset = train_ds.copy()
    line_dataset = line_dataset[line_dataset['product name'] == prod]
    return line_dataset



def update_viz(state):
    global prod_selected
    prod_selected = state.prod_selected

    state.properties_line_dataset =  {"x":prod_selected,
                                      "y[1]": "y",
                                      "y[2]": "yhat"} 
    state.line_dataset = state.line_dataset
    # state.scatter_dataset_pred = state.scatter_dataset_pred



dv_data_visualization_md = """
# Data **Visualization**{: .color-primary}
<|{dv_graph_selected}|toggle|lov={dv_graph_selector}|>

--------------------------------------------------------------------

<|part|render={dv_graph_selected == 'Line'}|
### Line
<|{prod_selected}|selector|lov={select_y}|dropdown|label=Select y|>
|>

<|{line_dataset}|chart|properties={properties_line_dataset}|rebuild|color[1]=red|color[2]=green|name[1]=Actual|name[2]=Predicted|mode=markers|type=line|height=600px|>

"""

