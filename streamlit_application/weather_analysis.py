import streamlit as st
from utils import fetch_current_weather, is_temperature_anomalous
from typing import Dict


def validate_api_key(api_key: str) -> Dict[str, str]:
    """
    Функция для проверки корректности поданного API-ключа.
    """
    if api_key:
        _, error = fetch_current_weather("Test City", api_key)
        if error and error.get("cod") == 401:
            st.session_state["api_key_valid"] = False

            return {
                "cod": "401",
                "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
            }

        else:
            st.session_state["api_key_valid"] = True

            return {
                "cod": "200",
                "message": "API-ключ корректен."
            }

    return {
        "cod": "400",
        "message": "Введите API-ключ для проверки."
    }


def run_weather_analysis() -> None:
    """
    Запускает анализ текущей погоды, включая проверку API-ключа,
    выбор города и отображение текущей температуры.
    """
    st.header("Текущая погода в городах")

    # Проверка загрузки данных
    if not st.session_state["data_loaded"]:
        st.warning("Сначала загрузите исторические данные на вкладке 'Анализ исторических данных'.")
        return

    # Ввод API-ключа (или используем сохраненный ключ из session_state, если он есть)
    api_key = st.text_input("Введите ваш API-ключ OpenWeatherMap",
                            value=st.session_state.get("api_key", ""))

    # Сохраняем введенный API-ключ в session_state
    if api_key:
        st.session_state["api_key"] = api_key

    # Проверка API-ключа
    if api_key:
        validation_status = validate_api_key(api_key)
        # Успешная проверка
        if validation_status["cod"] == "200":
            st.success(validation_status["message"])
        # Ошибка API-ключа
        elif validation_status["cod"] == "401":
            st.error(f"{validation_status}")
        # Другие ошибки
        else:
            st.warning(validation_status["message"])

    if not st.session_state.get("api_key_valid", False):
        st.warning("Введите корректный API-ключ для продолжения.")
        return

    # Выбор города
    historical_data = st.session_state["historical_data"]
    selected_city = st.selectbox("Выберите город", historical_data["city"].unique())

    # Получение текущей температуры
    current_temp, error = fetch_current_weather(selected_city, api_key)
    if error:
        st.error(error["message"])
    else:
        st.write(f"Текущая температура в {selected_city}: {current_temp}°C")
        city_data = historical_data[historical_data["city"] == selected_city]
        if is_temperature_anomalous(current_temp, selected_city, city_data):
            st.warning("Температура аномальна!")
        else:
            st.success("Температура в пределах нормы.")
