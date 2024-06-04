import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
                                                                                # Мы заранее выбрали STORE 1
    def preprocess_data(self, item_id, sales_data, calendar_data, prices_data): # Выбираем товар (item_id) из магазина STORE 1, подаем  df: sales, calendar, price
        item = item_id
        sales = sales_data

        ### Обрабатываем основную таблицу sales_data и отбираем ряд для конкретного товара

        customer = sales[(sales['store_id'] == 'STORE_1') & (sales['item_id'] == f'STORE_1_{item}')]
        customer = pd.merge(customer, calendar_data, on='date_id', how='inner')
        customer = customer.rename(columns={'date': 'ds', 'cnt': 'y'})
        customer = customer[['ds', 'y']]

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
        future_years = [2016, 2017]
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
    
    def train_model(self, df, holydays, test_size = 30):
        train_data = df.iloc[:test_size]
        test_data = df.iloc[test_size:]

        # Создание и обучение модели Prophet с праздниками и регрессором
        model = Prophet(holidays=holydays)
        model.add_regressor('price')

        # Обучение модели
        model.fit(train_data)
        return model, train_data, test_data

    def predict_and_evaluate(self, model, customer, period, test_data):
        # Создание прогноза для тестовой выборки
        future = model.make_future_dataframe(periods=period)
        # Объединяем данные о будущем с будущими ценами (предполагается, что у вас есть прогноз цен или просто используем последние известные цены)
        future = future.merge(customer[['ds', 'price']], on='ds', how='left')

        # Предсказание
        forecast = model.predict(future)

        # Выборка последних 30 дней прогноза
        predicted = forecast[['ds', 'yhat']].tail(period)

        # Метрики точности прогноза
        actual = test_data['y'].values
        predicted_values = predicted['yhat'].values

        mse = mean_squared_error(actual, predicted_values)
        mae = mean_absolute_error(actual, predicted_values)

        print(f'Mean Squared Error: {mse}')
        print(f'Mean Absolute Error: {mae}')

        # Визуализация прогноза
        fig1 = model.plot(forecast)
        plt.show()

        # Визуализация компонентов прогноза
        fig2 = model.plot_components(forecast)
        plt.show()

