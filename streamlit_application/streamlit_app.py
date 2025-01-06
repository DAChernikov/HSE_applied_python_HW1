import streamlit as st
from data_analysis import run_data_analysis
from weather_analysis import run_weather_analysis

st.set_page_config(page_title="Температурный Анализ", layout="wide")

# Инициализация состояния
if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False
if "historical_data" not in st.session_state:
    st.session_state["historical_data"] = None
if "api_key_valid" not in st.session_state:
    st.session_state["api_key_valid"] = False

# Главный интерфейс
st.title("Приложение анализа температур")

# Навигация между вкладками
tab = st.sidebar.radio("Выберите вкладку", ["Анализ исторических данных", "Текущая погода"])

# Обработка вкладок
if tab == "Анализ исторических данных":
    run_data_analysis()
elif tab == "Текущая погода":
    run_weather_analysis()
