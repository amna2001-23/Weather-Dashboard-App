# Weather Dashboard

Welcome to the Weather Dashboard app! This Streamlit application allows users to view current weather conditions and weather forecasts for cities around the world. The app also includes features for selecting specific countries, states/provinces, and cities, as well as a language translation option to view weather information in different languages.

## Features

- **Current Weather**: Displays real-time weather data for the selected city, including temperature, humidity, wind speed, and weather description.
- **Weather Forecast**: Provides a 5-day weather forecast with detailed information about each day and time.
- **Country, State/Province, and City Selection**: Users can select their desired location from a predefined list of countries, states/provinces, and cities.
- **Geolocation**: The app can detect the user's current location and display weather information for that location.
- **Language Translation**: Translate the weather details into different languages using the Google Translate API.
- **Interactive Charts**: Visualize weather data using interactive charts powered by Plotly.

## Getting Started

### Prerequisites

To run this application, you need to have the following installed:

- Python 3.8 or higher
- Streamlit
- Plotly
- Requests
- Geopy
- Googletrans

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/weather-dashboard.git
    cd weather-dashboard
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

### Usage

1. Open your web browser and go to `http://localhost:8501` to access the app.
2. Select your country, state/province, and city from the dropdown menus.
3. View the current weather and the 5-day forecast for your selected location.
4. Use the translation feature to view weather details in different languages.

### API

This app uses the [OpenWeatherMap API](https://openweathermap.org/api) to fetch real-time weather data and forecasts. You will need an API key from OpenWeatherMap to use the app.

### Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
