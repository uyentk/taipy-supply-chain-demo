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
    hist_dataset["%"] = (hist_dataset["Sales"] /hist_dataset["Sales"].sum()) * 100
    return hist_dataset

def top_N_prod_by_state(initial_dataset: pd.DataFrame, state: str, N = 10):
    state_dataset = initial_dataset[initial_dataset["Customer State"] == state]
    state_dataset = state_dataset.groupby("Product Name").agg(Sales = ('Sales', 'sum')).reset_index()
    state_dataset = state_dataset.sort_values(by='Sales', ascending= False).head(N)
    return state_dataset

def order_quantity_by_state(initial_dataset: pd.DataFrame, state: str, N = 10):
    state_dataset = initial_dataset[initial_dataset["Customer State"] == state]
    order_quantity_dataset = state_dataset.groupby("Product Name")['Order Item Quantity'].agg('sum').reset_index()
    order_quantity_dataset = order_quantity_dataset.sort_values(by='Order Item Quantity', ascending=False).head(N)
    return order_quantity_dataset

def update_map(state):
    global prod_selected
    prod_selected = state.prod_selected
    state.map_dataset_displayed = state.map_dataset_displayed

    state.properties_line_sales = {
        "x": "Date",
        "y": "Sales",
        "type": "line",
        "name": "Sales",
        "color": "#FAA0A0",
        "layout": {
            "xaxis": { "title": "" },
            "yaxis": { "title": "" },
        }
    }

    state.line_sales_dataset = state.line_sales_dataset

    state.hist_dataset = state.hist_dataset

def update_hist_state(state):
    global cus_state_selected
    cus_state_selected = state.cus_state_selected

    state.state_dataset = state.state_dataset 
    state.order_quantity_dataset = state.order_quantity_dataset
    

marker_map = {"color":"Sales", "size": "Size", "showscale":True, "colorscale":"lifeExp"}

layout_map = {
            "dragmode": "zoom",
            "mapbox": { "style": "open-street-map", "center": { "lat": 38, "lon": -90 }, "zoom": 3},
            "geo": {
            "scope": "usa"
        }
            }

properties_bar_state1 = {"orientation": "v",
                        "x": "Product Name",
                        "y": "Sales",
                        "layout": {"xaxis": { "title": "" }},
                        "color": "#FAA0A0"
                        }

properties_bar_state2 = {"orientation": "v",
                        "x": "Product Name",
                        "y": "Order Item Quantity",
                        "layout": {"xaxis": { "title": "" }},
                        "color": "A8D1D1"
                        }

options = {"unselected":{"marker":{"opacity":0.5}}}

marker_pie = {
    'colors': ["FD8A8A", "F1F7B5", "A8D1D1", "9EA1D4"]
}

dv_data_visualization_md = """
#**Data Visualization**{: .color-primary}

--------------------------------------------------------------------

<|{prod_selected}|selector|lov={select_prod}|dropdown|label=Select product|width = 3|>

#### **Doanh số theo bang**{: .color-primary}

<|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>

<|layout|columns=1 500px|
#### **Doanh số theo thời gian**{: .color-primary}

#### **Doanh số theo hình thức giao dịch**{: .color-primary}
|>

<|layout|columns=1 500px|
<|{line_sales_dataset}|chart|properties={properties_line_sales}|height=400px|>

<|{hist_dataset}|chart|type=pie|values=%|labels=Type|height=400px|marker={marker_pie}|>
|>

--------------------------------------------------------------------
<|{cus_state_selected}|selector|lov={select_state}|dropdown|label=Select customer state|width = 3|>

<|layout|columns=1 1|
#### **Top 10 sản phẩm có doanh số cao nhất theo bang**{: .color-primary}

#### **Top 10 sản phẩm được bán nhiều nhất theo bang**{: .color-primary}
|>

<|layout|columns=1 1|
<|{state_dataset}|chart|type=bar|properties={properties_bar_state1}|height=600px|>

<|{order_quantity_dataset}|chart|type=bar|properties={properties_bar_state2}|height=600px|>
|>
"""
#  Taipy currently doesn't support the choropleth map type directly
# <|{map_dataset_displayed}|chart|type=scattergeo|lat=Latitude|lon=Longitude|marker={marker_map}|layout={layout_map}|text=Text|mode=markers|height=800px|options={options}|>

