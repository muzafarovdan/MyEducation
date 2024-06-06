import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle
import os

class RetailSalesPredictor:
    def __init__(self, sales_data, calendar_data, prices_data):
        self.sales_data = sales_data
        self.calendar_data = calendar_data
        self.prices_data = prices_data

    def preprocess_data(self, store_id, item_id):
        # Фильтрация данных для конкретного магазина и товара
        sales = self.sales_data[(self.sales_data['store_id'] == store_id) & (self.sales_data['item_id'] == item_id)]
        sales = pd.merge(sales, self.calendar_data, on='date_id', how='inner')
        sales = sales.rename(columns={'date': 'ds', 'cnt': 'y'})
        sales['ds'] = pd.to_datetime(sales['ds'])

        # Обработка данных о праздниках
        holidays_1 = self.calendar_data[['date', 'event_name_1']].dropna().rename(columns={'date': 'ds', 'event_name_1': 'holiday'})
        holidays_2 = self.calendar_data[['date', 'event_name_2']].dropna().rename(columns={'date': 'ds', 'event_name_2': 'holiday'})
        holidays = pd.concat([holidays_1, holidays_2])
        holidays['ds'] = pd.to_datetime(holidays['ds'])

        # Добавление будущих дат праздников
        future_years = [2024, 2025]  # Пример будущих лет
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
        all_holidays = pd.concat([holidays, future_holidays_df])

        # Обработка данных о ценах
        item_prices = self.prices_data[self.prices_data['item_id'] == item_id][['wm_yr_wk', 'sell_price']]
        item_prices['wm_yr_wk'] = item_prices['wm_yr_wk'].astype(int)
        item_prices = item_prices.rename(columns={'wm_yr_wk': 'week', 'sell_price': 'price'})
        self.calendar_data['wm_yr_wk'] = self.calendar_data['wm_yr_wk'].astype(int)
        item_prices = item_prices.merge(self.calendar_data[['wm_yr_wk', 'date']], left_on='week', right_on='wm_yr_wk', how='left')
        item_prices = item_prices.rename(columns={'date': 'ds'}).drop(columns=['wm_yr_wk'])
        item_prices['ds'] = pd.to_datetime(item_prices['ds'])

        # Объединение данных о продажах и ценах
        sales = sales.merge(item_prices[['ds', 'price']], on='ds', how='left')

        return sales, all_holidays

    def train_model(self, sales_data, holidays, test_size=30):
        train_data = sales_data.iloc[:-test_size]
        test_data = sales_data.iloc[-test_size:]

        # Создание и обучение модели Prophet с праздниками и регрессором
        model = Prophet(holidays=holidays)
        model.add_regressor('price')
        model.fit(train_data)

        return model, train_data, test_data

    def predict_and_evaluate(self, model, sales_data, period, test_data):
        future = model.make_future_dataframe(periods=period)
        future = future.merge(sales_data[['ds', 'price']], on='ds', how='left')

        forecast = model.predict(future)
        predicted = forecast[['ds', 'yhat']].tail(period)

        actual = test_data['y'].values
        predicted_values = predicted['yhat'].values

        mse = mean_squared_error(actual, predicted_values)
        mae = mean_absolute_error(actual, predicted_values)

        print(f'Mean Squared Error: {mse}')
        print(f'Mean Absolute Error: {mae}')

        fig1 = model.plot(forecast)
        plt.show()

        fig2 = model.plot_components(forecast)
        plt.show()

        return mse, mae

    def save_model(self, model, filename):
        with open(filename, 'wb') as file:
            pickle.dump(model, file)

    def load_model(self, filename):
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        return model

    def forecast_period(self, store_id, item_id, period):
        sales_data, holidays = self.preprocess_data(store_id, item_id)
        model, train_data, test_data = self.train_model(sales_data, holidays)
        mse, mae = self.predict_and_evaluate(model, sales_data, period, test_data)
        return model, mse, mae

    def forecast_week(self, store_id, item_id):
        return self.forecast_period(store_id, item_id, period=7)

    def forecast_month(self, store_id, item_id):
        return self.forecast_period(store_id, item_id, period=30)

    def forecast_quarter(self, store_id, item_id):
        return self.forecast_period(store_id, item_id, period=90)

# # Использование класса
# # Загрузите данные о продажах, календарь и цены
# sales_data = ...  # Ваши данные о продажах
# calendar_data = ...  # Ваши данные календаря
# prices_data = ...  # Ваши данные о ценах

# predictor = RetailSalesPredictor(sales_data, calendar_data, prices_data)

# # Пример использования для магазина STORE_1 и товара STORE_1_1 на неделю
# model_week, mse_week, mae_week = predictor.forecast_week('STORE_1', 'STORE_1_1')
# print(f'Week - MSE: {mse_week}, MAE: {mae_week}')

# # Пример использования для магазина STORE_1 и товара STORE_1_1 на месяц
# model_month, mse_month, mae_month = predictor.forecast_month('STORE_1', 'STORE_1_1')
# print(f'Month - MSE: {mse_month}, MAE: {mae_month}')

# # Пример использования для магазина STORE_1 и товара STORE_1_1 на квартал
# model_quarter, mse_quarter, mae_quarter = predictor.forecast_quarter('STORE_1', 'STORE_1_1')
# print(f'Quarter - MSE: {mse_quarter}, MAE: {mae_quarter}')

# # Сохранение модели
# predictor.save_model(model_week, 'model_week.pkl')
# predictor.save_model(model_month, 'model_month.pkl')
# predictor.save_model(model_quarter, 'model_quarter.pkl')

# # Загрузка модели
# loaded_model_week = predictor.load_model('model_week.pkl')
# loaded_model_month = predictor.load_model('model_month.pkl')
# loaded_model_quarter = predictor.load_model('model_quarter.pkl')
