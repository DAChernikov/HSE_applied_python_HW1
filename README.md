# APPLIED PYTHON COURSE - HW1

Repository for completion of HW1 for "Applied Python" course at HSE university

### Repository contains:
* `Analyze_and_API.ipynb` - Jupyter-notebook of historycal cities' temperature analysis and API-testing part of HW1;
* `streamlit_application/streamlit_app.py` - main file to start StreamLit application of analysis history of weather in cities (from `csv-file`) and classification (anomaly or not) of current weather in cities;
* `streamlit_application/data_analysis.py` - contains functionality of "Анализ исторических данных" block in app;
* `streamlit_application/weather_analysis.py` - contains fuctionality of "Текущая погода" block in app;
* `streamlit_application/utils.py` - contains additional functionality of Streamlit app.

### Develop
Clone this repository to your local system (or create fork from this repo) and start developing new features!

### Usage
> `main` branch is connected to Streamlit Cloud service. It means that, all changes of this branch will be immediately deployed to Streamlit app on Streamlit Cloud. So, before merging changes from develop-branch to main you must perform tests of your changes and create pull-request.

App-link in Streamlit Cloud: https://hseappliedpythonhw1-app-dachernikov.streamlit.app

Go to the link and you will enter start-page of application. Then, follow the instructions:
1. You need to upload an `csv-file` with historical data of temperatures (example of that file you will find in `temperature_data.csv`). File must contain the following columns and data:
  - `city`: name of the city;
  - `timestamp`: day of recorded temperature;
  - `temperature`: mean daily temperature;
  - `season`: season of year (winter, spring, summer, autumn).

Example:
```csv
city,timestamp,temperature,season
New York,2010-01-01,1.6762708877717651,winter
New York,2010-01-02,6.5120215170556595,winter
New York,2010-01-03,-4.189094096250294,winter
New York,2010-01-04,-0.22599843655897517,winter
New York,2010-01-05,-0.06486291894632108,winter
New York,2010-01-06,0.8845866011361542,winter
```

2. After appliyng correct `csv-file`, app will show characteristics of file and weather-analysis of historical data. Moreover, you will see anomalies of temperature values in your dataset. After exploring results of analysis you can go to the next block of app.

3. Next block of app requires the uploaded `csv-file` from previous block and API key of [OpenWeatherMap](https://openweathermap.org). Without uploading historical data you won't do anything in this block, so, complete previous point to proceed next steps. If you uploaded your historical data, you will see space, where you will need to enter your API key for OpenWeatherMap (it's free to get, just visit page, sign-in, then go to `YOUR_PROFILE` -> `My API keys` and get your key for this app). After entering your key, you'll going to choose the city of your interest (from uploaded by you `csv-file` of historical data), then you will recieve the current temperature measure and classification - anomalious or not the current temperature that you recieved in app.

4. That's all. If you reload page, your progress in this app will be down, so you will need to upload `csv` and enter your API again (it makes your data, that you enter in app, secured)

### Contacts
  - `DAChernikov` - author and developer of this repository. Telegram: **@dachernikov** 🚀
