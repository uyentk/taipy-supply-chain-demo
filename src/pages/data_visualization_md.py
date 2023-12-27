import pandas as pd
import numpy as np


dv_graph_selector = ['Line', 'Map']
dv_graph_selected = dv_graph_selector[0]

# # Histograms dialog
# properties_histo_full = {}
# properties_scatter_dataset = {}

def creation_line_dataset(train_ds: pd.DataFrame):
    line_dataset = train_ds.copy()



# def creation_histo_full(test_dataset:pd.DataFrame):
#     """This function creates the dataset for the histogram plot.  For every column (except Exited), histo_full will have a positive and negative version.
#     The positive column will have NaN when the Exited is zero and the negative column will have NaN when the Exited is one. 

#     Args:
#         test_dataset (pd.DataFrame): the test dataset

#     Returns:
#         pd.DataFrame: the Dataframe used to display the Histogram
#     """
#     histo_full = test_dataset.copy()
    
#     for column in histo_full.columns:
#         column_neg = str(column)+'_neg'
#         histo_full[column_neg] = histo_full[column]
#         histo_full.loc[(histo_full['EXITED'] == 1),column_neg] = np.NaN
#         histo_full.loc[(histo_full['EXITED'] == 0),column] = np.NaN
        
#     return histo_full


def update_viz(state):
    global prod_selected
    prod_selected = state.prod_selected

    state.properties_line_dataset =  {"x":prod_selected,
                                      "y[1]": "y",
                                      "y[2]": "yhat"} 
    state.scatter_dataset = state.scatter_dataset
    state.scatter_dataset_pred = state.scatter_dataset_pred



dv_data_visualization_md = """
# Data **Visualization**{: .color-primary}
<|{dv_graph_selected}|toggle|lov={dv_graph_selector}|>

--------------------------------------------------------------------

<|part|render={dv_graph_selected == 'Line'}|
### Line
<|{prod_selected}|selector|lov={select_y}|dropdown|label=Select y|>
|>

<|{trained_infer}|chart|x=ds|y[1]=y|y[2]=yhat|>
|>

"""

