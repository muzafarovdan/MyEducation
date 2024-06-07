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
        # Вычисление week_id
        self.sales_data['week_id'] = (self.sales_data['date_id'] - 1) // 7 + 11101

        # Объединение таблиц
        merged_data = pd.merge(self.sales_data, self.prices_data, how='left', 
                               left_on=['store_id', 'item_id', 'week_id'], 
                               right_on=['store_id', 'item_id', 'wm_yr_wk'])
        merged_data.drop(columns=['wm_yr_wk'], inplace=True)

        customer = merged_data[(merged_data['store_id'] == store_id) & (merged_data['item_id'] == item_id)]
        customer = pd.merge(customer, self.calendar_data, on='date_id', how='inner')
        customer = customer.rename(columns={'date': 'ds', 'cnt': 'y'})
        customer['sell_price'].interpolate(method='linear', inplace=True)
        customer = customer[['ds', 'y', 'sell_price']]
        customer['ds'] = pd.to_datetime(customer['ds'])

        # Объединение столбцов event_name_1 и event_name_2
        self.calendar_data['event'] = self.calendar_data['event_name_1'].combine_first(self.calendar_data['event_name_2'])
        
        # Удаление строк, где нет праздников
        holidays_data = self.calendar_data.dropna(subset=['event'])
        
        # Преобразование в формат, подходящий для Prophet
        holidays = holidays_data[['date', 'event']].rename(columns={'date': 'ds', 'event': 'holiday'})
        
        return customer, holidays

    def train_model(self, sales_data, holidays, test_size=30):
        if len(sales_data) <= test_size:
            raise ValueError("Not enough data to train the model. Please provide more data.")

        train_data = sales_data.iloc[:-test_size]
        test_data = sales_data.iloc[-test_size:]

        if len(train_data) < 2:
            raise ValueError("Not enough data to train the model. Please provide more data.")

        model = Prophet(holidays=holidays, yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        model.add_regressor('sell_price')
        model.fit(train_data)

        return model, train_data, test_data

    def predict_and_evaluate(self, model, sales_data, test_data):
        future = model.make_future_dataframe(periods=len(test_data))
        future = future.merge(sales_data[['ds', 'sell_price']], on='ds', how='left')

        # Заполнение пропущенных значений в будущем датафрейме
        future['sell_price'].interpolate(method='linear', inplace=True)

        forecast = model.predict(future)
        forecast['yhat'] = forecast['yhat'].clip(lower=0)  # Ensure no negative predictions
        predicted = forecast[['ds', 'yhat']].tail(len(test_data))

        actual = test_data['y'].values
        predicted_values = predicted['yhat'].values

        mse = mean_squared_error(actual, predicted_values)
        mae = mean_absolute_error(actual, predicted_values)
        # Добавление малой константы к actual для вычисления MAPE
        mape = np.mean(np.abs((actual - predicted_values) / (actual + 0.001))) * 100

        print(f'Mean Squared Error: {mse}')
        print(f'Mean Absolute Error: {mae}')
        print(f'MAPE: {mape}%')

        fig1 = model.plot(forecast)
        plt.show()

        fig2 = model.plot_components(forecast)
        plt.show()

        # Визуализация тестовой части и предсказанных данных
        plt.figure(figsize=(10, 6))
        plt.plot(test_data['ds'], actual, label='Actual', marker='o')
        plt.plot(predicted['ds'], predicted_values, label='Predicted', marker='x')
        plt.title('Actual vs Predicted Sales')
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.legend()
        plt.show()

        return mse, mae, mape

    def save_model(self, model, filename):
        with open(filename, 'wb') as file:
            pickle.dump(model, file)

    def load_model(self, filename):
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        return model

    def forecast_period(self, store_id, item_id, period):
        sales_data, holidays = self.preprocess_data(store_id, item_id)
        available_data = len(sales_data)
        test_size = min(period, available_data - 2)  # Убедимся, что у нас достаточно данных для тренировки и тестирования
        if test_size < 1:
            raise ValueError("Not enough data to train the model for this period. Please provide more data.")
        model, train_data, test_data = self.train_model(sales_data, holidays, test_size=test_size)
        mse, mae, mape = self.predict_and_evaluate(model, sales_data, test_data)
        return model, mse, mae, mape

    def forecast_future(self, store_id, item_id, period):
        sales_data, holidays = self.preprocess_data(store_id, item_id)
        if len(sales_data) < 2:
            raise ValueError("Not enough data to forecast the future.")
        
        # Fill NaN values in the 'sell_price' column
        sales_data['sell_price'].fillna(method='ffill', inplace=True)
        
        train_data = sales_data.copy()
        model = Prophet(holidays=holidays)
        model.add_regressor('sell_price')
        model.fit(train_data)
        
        future = model.make_future_dataframe(periods=period)
        future = future.merge(sales_data[['ds', 'sell_price']], on='ds', how='left')
        
        # Fill NaN values in the 'sell_price' column in future data
        future['sell_price'].interpolate(method='linear', inplace=True)
        
        forecast = model.predict(future)
        forecast['yhat'] = forecast['yhat'].clip(lower=0)  # Ensure no negative predictions
        predicted = forecast[['ds', 'yhat']].tail(period)
        
        return predicted

    def forecast_week(self, store_id, item_id):
        return self.forecast_period(store_id, item_id, period=7)

    def forecast_month(self, store_id, item_id):
        return self.forecast_period(store_id, item_id, period=30)

    def forecast_quarter(self, store_id, item_id):
        return self.forecast_period(store_id, item_id, period=90)

    def predict_week(self, store_id, item_id):
        return self.forecast_future(store_id, item_id, period=7)

    def predict_month(self, store_id, item_id):
        return self.forecast_future(store_id, item_id, period=30)

    def predict_quarter(self, store_id, item_id):
        return self.forecast_future(store_id, item_id, period=90)
