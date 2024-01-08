import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import math

properties_line_dataset = {}

def creation_line_dataset(trained_infer: pd.DataFrame, prod: str):
    line_dataset = trained_infer.copy()
    line_dataset = line_dataset[line_dataset['product name'] == prod]
    return line_dataset

def rmse_calculation(trained_infer: pd.DataFrame, prod: str):
    table = trained_infer.copy()
    table = table[table['product name'] == prod]
    table['ds'] = pd.to_datetime(table['ds'])
    table = table[table['ds'] < '2017-09-30']
    predicted = table['yhat']
    actual = table['y']
    mse = mean_squared_error(actual, predicted)
    rmse = math.sqrt(mse)
    return rmse

def update_viz(state):
    global prod_selected
    prod_selected = state.prod_selected

    state.properties_line_dataset =  {"x":"ds",
                                      "y[1]": "y",
                                      "y[2]": "yhat",
                                      "type":"line",
                                      "color[1]": "#BADA55",
                                      "color[2]": "#FAA0A0",
                                      "name[1]": "Actual",
                                      "name[2]": "Predicted",
                                      "layout": {
                                          "xaxis": {"title": "Month"}
                                      }}
    
    state.line_dataset = state.line_dataset
    # state.line_dataset_res = state.line_dataset_res

    # state.properties_map_dataset = {'type':'scattergeo',
    #                                 'lat': 'Latitude',
    #                                 'lon': 'Longitude'}
    state.rmse = state.rmse
    # state.map_dataset_res = state.map_dataset_res

dv_model_management_md = """
#**Dashboard**{: .color-primary}

<|{prod_selected}|selector|lov={select_prod}|dropdown|label=Select product|width = 3|>

<|card|
**RMSE:**{: .color-primary .h7} <|{rmse}|text|class_name=h7|>

### **Doanh số theo thời gian**{: .color-primary}
<|{line_dataset}|chart|properties={properties_line_dataset}|height=600px|>
|>
"""
#  Taipy currently doesn't support the choropleth map type directly
# <|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>