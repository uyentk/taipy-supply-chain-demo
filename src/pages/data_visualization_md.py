import pandas as pd 
import numpy as np

properties_line_sales = {}
properties_hist_dataset = {}

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

def creation_line_sales(preprocessed_dataset: pd.DataFrame, prod: str):
    line_sales_dataset = preprocessed_dataset[preprocessed_dataset["Product Name"] == prod]
    return line_sales_dataset

def creation_hist_dataset(initial_dataset: pd.DataFrame, prod: str):
    hist_dataset = initial_dataset[initial_dataset['Product Name'] == prod]
    hist_dataset = hist_dataset.groupby(["Type"]).agg(Sales= ('Sales', 'sum')).reset_index()
    return hist_dataset
    
def update_map(state):
    global prod_selected
    prod_selected = state.prod_selected
    state.map_dataset_displayed = state.map_dataset_displayed

    state.properties_line_sales = {
        "x": "Date",
        "y": "Sales",
        "type": "line",
        "name": "Sales",
        "color": "#BADA55"
    }

    state.properties_hist_dataset = {
        "x": "Type",
        "y": "Sales",
    }

    state.line_sales_dataset = state.line_sales_dataset

    state.hist_dataset = state.hist_dataset

marker_map = {"color":"Sales", "size": "Size", "showscale":True, "colorscale":"lifeExp"}

layout_map = {
            "dragmode": "zoom",
            "mapbox": { "style": "open-street-map", "center": { "lat": 38, "lon": -90 }, "zoom": 3},
            "geo": {
            "scope": "usa"
        }
            }

options = {"unselected":{"marker":{"opacity":0.5}}}

dv_data_visualization_md = """
#**Map**{: .color-primary}

<|{prod_selected}|selector|lov={select_prod}|dropdown|label=Select product|width = 3|>

### **Doanh số theo bang**{: .color-primary}

# <|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>

<|{line_sales_dataset}|chart|properties={properties_line_sales}|height=600px|>

<|{hist_dataset}|chart|type=bar|properties = {properties_hist_dataset}|height=600px|>
"""
#  Taipy currently doesn't support the choropleth map type directly
# <|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>




