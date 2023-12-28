from taipy import Config, Scope
##############################################################################################################################
# Creation of the datanodes
##############################################################################################################################
# How to connect to the database
path_to_csv = 'data\DataCoSupplyChainDataset.csv'


from prophet import Prophet

import pandas as pd
import datetime as dt

def preprocess_dataset(initial_dataset: pd.DataFrame):
    # convert to datetime type and extract only date part
    initial_dataset["DateOrders"] = pd.to_datetime(initial_dataset['order date (DateOrders)'], format='%m/%d/%Y %H:%M').dt.date
    # modify format of DateOrders 
    initial_dataset['DateOrders'] = pd.to_datetime(initial_dataset['DateOrders']).dt.strftime('%d/%m/%Y')
    initial_dataset.drop(columns='order date (DateOrders)', inplace=True)

    # Extract month & year from DateOrders
    initial_dataset['DateOrders_month'] = pd.to_datetime(initial_dataset['DateOrders'], format= '%d/%m/%Y').dt.month
    initial_dataset['DateOrders_year'] = pd.to_datetime(initial_dataset['DateOrders'], format= '%d/%m/%Y').dt.year

    def create_month_year(row):
        month_year = str(row['DateOrders_month']) + '/' + str(row['DateOrders_year'])
        return month_year
    
    # Sales in terms of product name each month
    sales_product_month = initial_dataset.groupby(['Product Name', 'DateOrders_month', 'DateOrders_year']) \
                                            .agg({'Sales': 'sum'}) \
                                            .reset_index()
    
    sales_product_month['DateOrders_month_year'] = sales_product_month.apply(create_month_year, axis = 1)
    sales_product_month = sales_product_month.sort_values(by=['Product Name', 'DateOrders_year', 'DateOrders_month'])

    # convert to datetime with dayfirst = True
    datetime_series = pd.to_datetime(sales_product_month['DateOrders_month_year'], format = '%m/%Y', errors = 'coerce', dayfirst = True)
    sales_product_month['Date'] = datetime_series.dt.strftime('%d/%m/%Y')

    # drop unneeded columns
    sales_product_month.drop(columns = {'DateOrders_month', 'DateOrders_year', 'DateOrders_month_year'}, inplace=True)

    sales_product_month = sales_product_month[sales_product_month['Date'] != '01/10/2017']

    print("Preprocessing done!\n")
    return sales_product_month


# def create_train_df(preprocessed_data: pd.DataFrame, prod: str, end_date: dt.datetime):
#     print(f'Processing {prod}...')
#     tmp_df = preprocessed_data[preprocessed_data['Product Name'] == prod]
#     tmp_df['Date'] = pd.to_datetime(tmp_df['Date']).dt.strftime('%Y-%d-%m')
#     tmp_df.drop(columns='Product Name', inplace=True)
    
#     start_date = tmp_df['Date'].min()
#     date_range = pd.date_range(start=start_date, end=end_date, freq='1M') - pd.offsets.MonthBegin(1)
#     empty_df = pd.DataFrame({'Date': date_range})
#     empty_df['Date'] = empty_df['Date'].astype(str)
    
#     full_date_df = pd.merge(empty_df, tmp_df, on='Date', how='left')
#     full_date_df['Sales'] = full_date_df['Sales'].fillna(0)
    
#     train_df = full_date_df[['Date', 'Sales']].rename(columns={'Date': 'ds', 'Sales': 'y'})
#     train_df = train_df[train_df['ds'] < '2017-10-01']

#     return train_df 

# def train_infer(preprocessed_data: pd.DataFrame):
#     end_date = '2017-12-01'
#     end_date = pd.to_datetime(pd.Series(end_date))[0]
    

#     result_df = pd.DataFrame(columns=['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'product name', 'y'])

#     # Products ordered in more than 10 months
#     tmp = preprocessed_data['Product Name'].value_counts().reset_index()
#     product_ls = tmp[tmp['count'] > 10]['Product Name'].unique()

#     # training & inference
#     for prod in product_ls:
#         train_df = create_train_df(preprocessed_data, prod, end_date)

#         m = Prophet(
#             changepoint_prior_scale=0.001,
#             seasonality_prior_scale=0.1
#         )
#         m.fit(train_df)

#         # Infer
#         future = m.make_future_dataframe(periods=4, freq='M')
#         forecast = m.predict(future)
        
#         forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
#         forecast['product name'] = prod
#         forecast['y'] = train_df['y']
        
#         result_df = pd.concat([result_df, forecast], ignore_index=True)

#     return result_df

def train_infer(preprocessed_data: pd.DataFrame):
    end_date = '2017-12-01'
    end_date = pd.to_datetime(pd.Series(end_date))[0]

    result_df = pd.DataFrame(columns=['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'product name'])

    # Products ordered in more than 10 months
    tmp = preprocessed_data['Product Name'].value_counts().reset_index()
    product_ls = tmp[tmp['count'] > 10]['Product Name'].unique()
    
    for prod in product_ls:
        tmp_df = preprocessed_data[preprocessed_data['Product Name'] == prod]
        tmp_df['Date'] = pd.to_datetime(tmp_df['Date']).dt.strftime('%Y-%d-%m')
        tmp_df.drop(columns='Product Name', inplace=True)
        
        start_date = tmp_df['Date'].min()
        date_range = pd.date_range(start=start_date, end=end_date, freq='1M') - pd.offsets.MonthBegin(1)
        empty_df = pd.DataFrame({'Date': date_range})
        empty_df['Date'] = empty_df['Date'].astype(str)
        
        full_date_df = pd.merge(empty_df, tmp_df, on='Date', how='left')
        full_date_df['Sales'] = full_date_df['Sales'].fillna(0)
        
        train_df = full_date_df[['Date', 'Sales']].rename(columns={'Date': 'ds', 'Sales': 'y'})
        train_df = train_df[train_df['ds'] < '2017-10-01']

        m = Prophet(
            changepoint_prior_scale=0.001,
            seasonality_prior_scale=0.1
        )
        m.fit(train_df)

        # Infer
        future = m.make_future_dataframe(periods=4, freq='M')
        forecast = m.predict(future)
        
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast['product name'] = prod
        forecast['y'] = train_df['y']
        
        result_df = pd.concat([result_df, forecast], ignore_index=True)

    return result_df
# ======================== CONFIG ========================

# path for csv and file_path for pickle
initial_dataset_cfg = Config.configure_csv_data_node(id="initial_dataset",
                                             default_path=path_to_csv,
                                             encoding="latin1",
                                             has_header=True)

# end_date_cfg = Config.configure_data_node(id= "end_date")
# prod_cfg = Config.configure_data_node(id= "prod")
preprocessed_dataset_cfg = Config.configure_data_node(id="preprocessed_dataset")

# the final datanode that contains the processed data
# train_dataset_cfg = Config.configure_data_node(id="train_dataset")

# the final datanode that contains the processed data
# trained_model_ml_cfg = Config.configure_data_node(id="trained_model_ml")
trained_infer_cfg= Config.configure_data_node(id="trained_infer")


##############################################################################################################################
# Creation of the tasks
##############################################################################################################################

# the task will make the link between the input data node 
# and the output data node while executing the function

# initial_dataset --> preprocess dataset --> preprocessed_dataset
task_preprocess_dataset_cfg = Config.configure_task(id="preprocess_dataset",
                                                    input=initial_dataset_cfg,
                                                    function=preprocess_dataset,
                                                    output=preprocessed_dataset_cfg)

# preprocessed_dataset --> create train data --> train_dataset
# task_create_train_cfg = Config.configure_task(id="create_train_data",
#                                                    input=[preprocessed_dataset_cfg, prod_cfg, end_date_cfg],
#                                                    function=create_train_df,
#                                                    output=[train_dataset_cfg])


# train_dataset --> create train_model data --> trained_model
task_train_infer_model_cfg = Config.configure_task(id="train_infer_model",
                                                      input= preprocessed_dataset_cfg,
                                                      function=train_infer,
                                                      output=trained_infer_cfg)
        
##############################################################################################################################
# Creation of the scenario
##############################################################################################################################

scenario_cfg = Config.configure_scenario(id="supplychain_predict",
                                         task_configs=[task_preprocess_dataset_cfg,
                                                    #    task_create_train_cfg,
                                                       task_train_infer_model_cfg,
                                                       ])

Config.export('taipy-supply-chain-demo/src/config/config_supply.toml')