import pandas as pd
import numpy as np


dv_graph_selector = ['Line', 'Map']
dv_graph_selected = dv_graph_selector[0]

# # Histograms dialog
# properties_histo_full = {}
properties_line_dataset = {}

def creation_line_dataset(trained_infer: pd.DataFrame, prod: str):
    line_dataset = trained_infer.copy()
    line_dataset = line_dataset[line_dataset['product name'] == prod]
    return line_dataset

def creation_map_dataset(initial_dataset: pd.DataFrame, prod: str):
    map_dataset = initial_dataset.copy()
    map_dataset = map_dataset[map_dataset['Product Name'] == prod]
    map_dataset = (
        map_dataset.groupby(['Customer State',
                              'Latitude',
                              'Longitude'
                              ])
                   .agg(Sales=('Sales', 'sum'))
                   .reset_index()
    )
    map_dataset_displayed = map_dataset[map_dataset['Sales'] > 2000]
    # map_dataset_displayed = map_dataset[map_dataset['Sales'] > 10]
    solve = np.linalg.solve([[map_dataset_displayed["Sales"].min(), 1], [map_dataset_displayed["Sales"].max(), 1]],
                           [5, 60])
    # map_dataset_displayed['Size'] = np.sqrt(map_dataset_displayed.loc[:,'Sales']/map_dataset_displayed.loc[:,'Sales'].max())* 10 
    map_dataset_displayed["Size"] = map_dataset_displayed["Sales"].apply(lambda p: 1.25*p*solve[0]+solve[1])
    map_dataset_displayed['Text'] = map_dataset_displayed.loc[:,'Sales'].astype(str) + ' orders </br> ' + map_dataset_displayed.loc[:,'Customer State']
    return map_dataset_displayed

def update_viz(state):
    global prod_selected
    prod_selected = state.prod_selected

    state.properties_line_dataset =  {"x":"ds",
                                      "y[1]": "y",
                                      "y[2]": "yhat",
                                      "type":"line",
                                      "color[1]": "green",
                                      "color[2]": "red",
                                      "name[1]": "Actual",
                                      "name[2]": "Predicted"}
    
    state.line_dataset = state.line_dataset
    # state.line_dataset_res = state.line_dataset_res

    # state.properties_map_dataset = {'type':'scattergeo',
    #                                 'lat': 'Latitude',
    #                                 'lon': 'Longitude'}
    
    state.map_dataset_displayed = state.map_dataset_displayed
    # state.map_dataset_res = state.map_dataset_res

marker_map = {"color":"Sales", "size": "Size", "showscale":True, "colorscale":"Viridis"}

layout_map = {
            "dragmode": "zoom",
            "mapbox": { "style": "open-street-map", "center": { "lat": 38, "lon": -90 }, "zoom": 3},
            "geo": {
            "scope": "usa"
        }
            }

options = {"unselected":{"marker":{"opacity":0.5}}}

dv_data_visualization_md = """
# Data **Visualization**{: .color-primary}
<|{dv_graph_selected}|toggle|lov={dv_graph_selector}|>

--------------------------------------------------------------------

<|part|render={dv_graph_selected == 'Line'}|
### Line
<|{prod_selected}|selector|lov={select_prod}|dropdown|label=Select product|>
|>

<|{line_dataset}|chart|properties={properties_line_dataset}|height=600px|>

--------------------------------------------------------------------

<|part|render={dv_graph_selected == 'Map'}|
### Map
<|{prod_selected}|selector|lov={select_prod}|dropdown|label=Select product|>
|>

# <|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>
"""
#  Taipy currently doesn't support the choropleth map type directly
# <|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>