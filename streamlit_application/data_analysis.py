import streamlit as st
import pandas as pd
from utils import calculate_city_stats, plot_temp_stats, plot_seasonal_profile


def run_data_analysis() -> None:
    """
    Запускает анализ исторических данных, включая загрузку данных,
    выбор города и вычисление статистики.
    """
    st.header("Анализ исторических данных")

    # Загрузка данных
    uploaded_file = st.file_uploader("Загрузите CSV-файл с историческими данными", type="csv")
    if uploaded_file:
        data = pd.read_csv(uploaded_file, parse_dates=["timestamp"], infer_datetime_format=True)
        data["season"] = data["season"].astype(str)

        # Сохранение данных в состояние
        st.session_state["data_loaded"] = True
        st.session_state["historical_data"] = data

    if st.session_state["data_loaded"]:
        data = st.session_state["historical_data"]
        st.write("Пример данных:", data.sample(10))

        # Выбор города
        selected_city = st.selectbox("Выберите город", sorted(data["city"].unique()))
        city_data = data[data["city"] == selected_city]

        # Анализ данных
        stats = calculate_city_stats(city_data)
        st.write(f"Средняя температура: {stats['mean_temp']:.2f}°C")
        st.write(f"Минимальная температура: {stats['min_temp']:.2f}°C")
        st.write(f"Максимальная температура: {stats['max_temp']:.2f}°C")
        st.write(f"Тренд температуры: {'положительный' if stats['trend'] > 0 else 'отрицательный'}")

        # Временной ряд
        st.subheader("Временной ряд температур с аномалиями")
        plot_temp_stats(stats["data"], selected_city)

        # Сезонный профиль
        st.subheader("Сезонный профиль")
        plot_seasonal_profile(stats["seasonal_profile"], selected_city)

        # Сохраняем сезонные статистики
        season_stats = data.groupby(["city", "season"])["temperature"].agg(["mean", "std"]).reset_index()
        st.session_state["season_stats"] = season_stats
