import pandas as pd
import requests
import streamlit as st
from typing import Dict, Tuple, Optional
from sklearn.linear_model import LinearRegression


def calculate_city_stats(data: pd.DataFrame) -> Dict[str, object]:
    """
    Функция для вычисления статистики по городским данным: средняя, минимальная и максимальная
    температура, тренд, сезонный профиль, аномалии.
    """
    data["rolling_mean"] = data["temperature"].rolling(window=30, min_periods=1).mean()
    data["rolling_std"] = data["temperature"].rolling(window=30, min_periods=1).std()
    data["anomaly"] = abs(data["temperature"] - data["rolling_mean"]) > 2 * data["rolling_std"]

    reg = LinearRegression()
    reg.fit(data.index.values.reshape(-1, 1), data["temperature"].values)
    trend = reg.coef_[0]

    seasonal_profile = data.groupby("season")["temperature"].agg(["mean", "std"]).reset_index()

    return {
        "data": data,
        "mean_temp": data["temperature"].mean(),
        "min_temp": data["temperature"].min(),
        "max_temp": data["temperature"].max(),
        "trend": trend,
        "seasonal_profile": seasonal_profile,
    }


def plot_temp_stats(data: pd.DataFrame, city: str) -> None:
    """
    Строит график временного ряда температур с выделением аномалий.
    """
    import plotly.graph_objects as go

    fig = go.Figure()

    # Основной тренд
    fig.add_trace(go.Scatter(
        x=data["timestamp"], y=data["temperature"], mode="lines", name="Temperature"
    ))

    # Аномалии
    anomalies = data[data["anomaly"]]
    fig.add_trace(go.Scatter(
        x=anomalies["timestamp"], y=anomalies["temperature"], mode="markers",
        name="Аномалии", marker=dict(color="red", size=8)
    ))

    fig.update_layout(
        title=f"Температурный тренд: {city}",
        xaxis_title="Дата",
        yaxis_title="Температура (°C)"
    )
    st.plotly_chart(fig)


def plot_seasonal_profile(profile: pd.DataFrame, city: str) -> None:
    """
    Строит график сезонного профиля температур.
    """
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=profile["season"], y=profile["mean"],
        error_y=dict(type="data", array=profile["std"]),
        name="Средняя температура"
    ))

    fig.update_layout(
        title=f"Сезонный профиль: {city}",
        xaxis_title="Сезон",
        yaxis_title="Температура (°C)"
    )
    st.plotly_chart(fig)


def fetch_current_weather(city: str, api_key: str) \
        -> Tuple[Optional[float], Optional[Dict[str, str]]]:
    """
    Функция для получения текущей температуры через OpenWeatherMap API.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") != 200:
            return None, response
        return response["main"]["temp"], None
    except Exception as e:
        return None, {"message": str(e)}


def is_temperature_anomalous(temp: float, city: str, historical_data: pd.DataFrame) -> bool:
    """
    Проверяет, является ли текущая температура аномальной для выбранного города.
    """
    city_stats = historical_data[historical_data["city"] == city]
    if city_stats.empty:
        return False

    mean_temp = city_stats["temperature"].mean()
    std_temp = city_stats["temperature"].std()
    return abs(temp - mean_temp) > 2 * std_temp
