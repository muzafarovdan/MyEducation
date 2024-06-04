import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle
import os


# # Использование класса
# sales_data = ...  # Загрузите данные о продажах
# calendar_data = ...  # Загрузите данные календаря
# prices_data = ...  # Загрузите данные о ценах

# preprocessor = DataPreprocessor(sales_data, calendar_data, prices_data)

class RetailSalesPredictor:
    def __init__(self, sales_data, calendar_data, prices_data):
        self.sales_data = sales_data
        self.calendar_data = calendar_data
        self.prices_data = prices_data

    def preprocess_data(self, item_id, sales_data, calendar_data, prices_data): # Выбираем товар, подаем df: sales, 
        item = item_id
        sales = sales_data
        
        ### Обрабатываем основную таблицу 

        customer = sales[(sales['store_id'] == 'STORE_1') & (sales['item_id'] == f'STORE_1_{item}')]
        customer = customer.rename(columns={'date': 'ds', 'cnt': 'y'})
        customer = customer.sort_values('ds')

        customer['ds'] = pd.to_datetime(customer['ds'])

        ### Обрабатываем праздники

        # Извлекаем даты и названия праздников
        holidays_1 = calendar_data[['date', 'event_name_1']].dropna().rename(columns={'date': 'ds', 'event_name_1': 'holiday'})
        holidays_2 = calendar_data[['date', 'event_name_2']].dropna().rename(columns={'date': 'ds', 'event_name_2': 'holiday'})

        # Объединяем оба набора данных
        holidays = pd.concat([holidays_1, holidays_2])

        # Убедимся, что столбец ds имеет тип datetime
        holidays['ds'] = pd.to_datetime(holidays['ds'])

        # Создание DataFrame с будущими датами праздников
        future_years = [2024, 2025, 2026]
        future_holidays = []

        for year in future_years:
            for holiday in holidays['holiday'].unique():
                future_holidays.append({
                    'holiday': holiday,
                    'ds': pd.to_datetime(f"{year}-01-01"),  # Здесь нужно указать соответствующие даты праздников
                    'lower_window': 0,
                    'upper_window': 1
                })

        future_holidays_df = pd.DataFrame(future_holidays)
        # Объединяем текущие и будущие праздники
        all_holidays = pd.concat([holidays, future_holidays_df])

        ###  Обрабатываем цены

        item_prices = prices_data[prices_data['item_id'] == f'STORE_1_{item}'][['wm_yr_wk', 'sell_price']]

        # Убедимся, что wm_yr_wk в формате целого числа
        item_prices['wm_yr_wk'] = item_prices['wm_yr_wk'].astype(int)

        # Переименовываем столбцы для удобства
        item_prices = item_prices.rename(columns={'wm_yr_wk': 'week', 'sell_price': 'price'})

        # Добавляем даты в данные о ценах, если у нас есть календарь с недельным номером и датами
        calendar_data['wm_yr_wk'] = calendar_data['wm_yr_wk'].astype(int)
        item_prices = item_prices.merge(calendar_data[['wm_yr_wk', 'date']], left_on='week', right_on='wm_yr_wk', how='left')
        item_prices = item_prices.rename(columns={'date': 'ds'}).drop(columns=['wm_yr_wk'])

        # Убедимся, что столбец ds имеет тип datetime
        item_prices['ds'] = pd.to_datetime(item_prices['ds'])

        # Убедимся, что столбец ds имеет тип datetime и в customer
        customer['ds'] = pd.to_datetime(customer['ds'])

        # Объединение данных о продажах и ценах
        customer = customer.merge(item_prices[['ds', 'price']], on='ds', how='left')

        return f'STORE_1_{item}', customer, all_holidays














    
    def train_model(self):
        for item_id in self.data['item_id'].unique():
            item_data = self.data[self.data['item_id'] == item_id]
            model = Prophet(holidays=self.holidays)
            model.fit(item_data)
            self.models[item_id] = model
    
    def evaluate_model(self, test_data):
        mse_list = []
        mae_list = []
        
        for item_id in self.models.keys():
            item_test_data = test_data[(test_data['store_id'] == self.store_id) & (test_data['item_id'] == item_id)]
            item_test_data = item_test_data.rename(columns={'date': 'ds', 'sales': 'y'})
            
            future = self.models[item_id].make_future_dataframe(periods=len(item_test_data))
            forecast = self.models[item_id].predict(future)
            forecast = forecast[['ds', 'yhat']].tail(len(item_test_data))
            
            actual = item_test_data['y'].values
            predicted = forecast['yhat'].values
            
            mse = mean_squared_error(actual, predicted)
            mae = mean_absolute_error(actual, predicted)
            
            mse_list.append(mse)
            mae_list.append(mae)
        
        return np.mean(mse_list), np.mean(mae_list)
    
    def save_model(self, path):
        with open(os.path.join(path, f'model_store_{self.store_id}.pkl'), 'wb') as f:
            pickle.dump(self.models, f)
    
    def load_model(self, path):
        with open(os.path.join(path, f'model_store_{self.store_id}.pkl'), 'rb') as f:
            self.models = pickle.load(f)
    
    def predict_sales(self, periods):
        predictions = {}
        
        for item_id, model in self.models.items():
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            predictions[item_id] = forecast[['ds', 'yhat']].tail(periods)
        
        return predictions
