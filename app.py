import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from geopy.geocoders import Nominatim
from googletrans import Translator

# Sample local dataset for country, state, and city selection (same as provided)
country_data = {
    "Pakistan": {
        "Punjab": [
            "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala", "Gujrat",
            "Sialkot", "Sheikhupura", "Rahim Yar Khan", "Jhang", "Dera Ghazi Khan",
            "Sahiwal", "Kasur", "Okara", "Chiniot", "Kamoke", "Hafizabad", "Sadiqabad",
            "Burewala", "Khanewal", "Muzaffargarh", "Mandi Bahauddin", "Jhelum",
            "Khanpur", "Pakpattan", "Daska", "Gojra", "Muridke", "Bahawalnagar",
            "Samundri", "Jaranwala", "Chishtian", "Attock", "Vehari", "Kot Abdul Malik",
            "Ferozewala", "Chakwal", "Gujranwala Cantonment", "Kamalia", "Ahmedpur East",
            "Kot Addu", "Wazirabad", "Layyah", "Taxila", "Khushab", "Mianwali",
            "Lodhran", "Hasilpur", "Bhakkar", "Arif Wala", "Sambrial", "Jatoi",
            "Haroonabad", "Narowal", "Bhalwal", "Jallah Jeem"
        ],
        "Sindh": [
            "Karachi", "Hyderabad", "Sukkur", "Larkana", "Mirpurkhas"
        ],
        "Khyber Pakhtunkhwa": [
            "Peshawar", "Mardan", "Abbottabad", "Swat", "Dera Ismail Khan"
        ],
        "Balochistan": [
            "Quetta", "Gwadar", "Kalat", "Khuzdar", "Panjgur"
        ],
        "Gilgit-Baltistan": [
            "Gilgit", "Skardu", "Hunza", "Astore", "Diamer"
        ],
        "Azad Jammu and Kashmir": [
            "Muzaffarabad", "Rawalakot", "Neelum", "Bagh", "Kotli"
        ]
    },

    "United States": {
        "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose"],
        "Texas": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"],
        "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville", "St. Petersburg"],
        "New York": ["New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse"],
        "Illinois": ["Chicago", "Aurora", "Naperville", "Springfield", "Peoria"]
    },
    "China": {
        "Guangdong": ["Guangzhou", "Shenzhen", "Dongguan", "Zhuhai", "Foshan"],
        "Jiangsu": ["Nanjing", "Suzhou", "Wuxi", "Xuzhou", "Yangzhou"],
        "Shandong": ["Jinan", "Qingdao", "Yantai", "Weihai", "Zibo"],
        "Henan": ["Zhengzhou", "Luoyang", "Kaifeng", "Anyang", "Xinyang"],
        "Sichuan": ["Chengdu", "Mianyang", "Deyang", "Leshan", "Zigong"]
    },
    "Russia": {
        "Moscow": ["Moscow"],
        "St. Petersburg": ["St. Petersburg"],
        "Siberia": ["Novosibirsk", "Omsk", "Krasnoyarsk", "Irkutsk", "Ulan-Ude"],
        "Ural": ["Yekaterinburg", "Chelyabinsk", "Perm", "Tyumen", "Kurgan"],
        "Far East": ["Vladivostok", "Khabarovsk", "Sakhalin", "Magadan", "Petropavlovsk-Kamchatsky"]
    },
    "India": {
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
        "West Bengal": ["Kolkata", "Howrah", "Siliguri", "Durgapur", "Asansol"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli-Dharwad", "Mangalore", "Belgaum"]
    },
    "Germany": {
        "Bavaria": ["Munich", "Nuremberg", "Augsburg", "Regensburg", "Würzburg"],
        "North Rhine-Westphalia": ["Düsseldorf", "Cologne", "Essen", "Dortmund", "Bonn"],
        "Baden-Württemberg": ["Stuttgart", "Mannheim", "Heidelberg", "Freiburg", "Ulm"],
        "Hesse": ["Frankfurt", "Wiesbaden", "Kassel", "Darmstadt", "Offenbach"],
        "Saxony": ["Dresden", "Leipzig", "Chemnitz", "Görlitz", "Freiberg"]
    },
    "Japan": {
        "Tokyo": ["Tokyo"],
        "Osaka": ["Osaka"],
        "Kyoto": ["Kyoto"],
        "Hokkaido": ["Sapporo", "Hakodate", "Asahikawa", "Obihiro", "Kushiro"],
        "Fukuoka": ["Fukuoka", "Kitakyushu", "Kurume", "Yanagawa", "Nagasaki"]
    },
    "United Kingdom": {
        "England": ["London", "Manchester", "Birmingham", "Liverpool", "Sheffield"],
        "Scotland": ["Edinburgh", "Glasgow", "Aberdeen", "Dundee", "Inverness"],
        "Wales": ["Cardiff", "Swansea", "Newport", "Wrexham", "Bangor"],
        "Northern Ireland": ["Belfast", "Derry", "Lisburn", "Armagh", "Newry"]
    },
    "France": {
        "Île-de-France": ["Paris", "Boulogne-Billancourt", "Versailles", "Créteil", "Saint-Denis"],
        "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Toulon", "Aix-en-Provence", "Avignon"],
        "Auvergne-Rhône-Alpes": ["Lyon", "Clermont-Ferrand", "Grenoble", "Saint-Étienne", "Annecy"],
        "Nouvelle-Aquitaine": ["Bordeaux", "Limoges", "Poitiers", "La Rochelle", "Périgueux"],
        "Occitanie": ["Toulouse", "Montpellier", "Nîmes", "Perpignan", "Carcassonne"]
    },
    "Brazil": {
        "São Paulo": ["São Paulo", "Guarulhos", "Campinas", "Sorocaba", "São Bernardo do Campo"],
        "Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Nova Iguaçu", "Duque de Caxias", "Belford Roxo"],
        "Minas Gerais": ["Belo Horizonte", "Uberlândia", "Juiz de Fora", "Montes Claros", "Contagem"],
        "Bahia": ["Salvador", "Feira de Santana", "Itabuna", "Vitória da Conquista", "Lauro de Freitas"],
        "Amazonas": ["Manaus", "Parintins", "Itacoatiara", "Coari", "Tefé"]
    },
    "Canada": {
        "Ontario": ["Toronto", "Ottawa", "Hamilton", "London", "Windsor"],
        "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau", "Trois-Rivières"],
        "British Columbia": ["Vancouver", "Victoria", "Surrey", "Burnaby", "Richmond"],
        "Alberta": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
        "Manitoba": ["Winnipeg", "Brandon", "Thompson", "Steinbach", "Selkirk"]
    },
    "Australia": {
        "New South Wales": ["Sydney", "Newcastle", "Wollongong", "Central Coast", "Coffs Harbour"],
        "Victoria": ["Melbourne", "Geelong", "Ballarat", "Bendigo", "Shepparton"],
        "Queensland": ["Brisbane", "Gold Coast", "Townsville", "Cairns", "Sunshine Coast"],
        "Western Australia": ["Perth", "Mandurah", "Bunbury", "Geraldton", "Kalgoorlie"],
        "South Australia": ["Adelaide", "Mount Gambier", "Whyalla", "Port Pirie", "Port Lincoln"]
    },
    "Saudi Arabia": {
        "Riyadh": ["Riyadh"],
        "Makkah": ["Mecca", "Jeddah", "Taif", "Khulais", "Al-Leith"],
        "Madinah": ["Medina", "Yanbu", "Al-Ula", "Khaybar", "Badr"],
        "Eastern Province": ["Dhahran", "Khobar", "Dammam", "Jubail", "Ahsa"],
        "Asir": ["Abha", "Khamis Mushait", "Baljurashi", "Bisha", "Mahayil Asir"]
    },
    "South Korea": {
        "Seoul": ["Seoul"],
        "Busan": ["Busan"],
        "Incheon": ["Incheon"],
        "Gyeonggi-do": ["Suwon", "Goyang", "Yongin", "Seongnam", "Ansan"],
        "North Jeolla": ["Jeonju", "Iksan", "Wanju", "Gunsan", "Namwon"]
    },
    "Mexico": {
        "Mexico City": ["Mexico City"],
        "Jalisco": ["Guadalajara", "Tepatitlán", "Puerto Vallarta", "Tepatitlán", "Lagos de Moreno"],
        "Nuevo León": ["Monterrey", "San Pedro Garza García", "Guadalupe", "Apodaca", "Santa Catarina"],
        "Puebla": ["Puebla", "Tehuacán", "Cholula", "Atlixco", "San Martín Texmelucan"],
        "Yucatán": ["Mérida", "Valladolid", "Tizimin", "Progreso", "Motul"]
    },
    "Italy": {
        "Lazio": ["Rome", "Frosinone", "Latina", "Viterbo", "Rieti"],
        "Lombardy": ["Milan", "Bergamo", "Brescia", "Monza", "Pavia"],
        "Campania": ["Naples", "Salerno", "Caserta", "Avellino", "Benevento"],
        "Sicily": ["Palermo", "Catania", "Messina", "Syracuse", "Trapani"],
        "Veneto": ["Venice", "Verona", "Vicenza", "Padua", "Rovigo"]
    }
    # Add more countries, states/provinces, and cities here
}


# Set up the Streamlit app
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city, units="metric"):
    api_key = "7f7ed66cf9b9d37c36911a304ba2124a"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
    response = requests.get(url)
    return response.json()

# Function to get forecast data from OpenWeatherMap API
def get_forecast_data(city, units="metric"):
    api_key = "7f7ed66cf9b9d37c36911a304ba2124a"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={api_key}"
    response = requests.get(url)
    return response.json()

# Function to display weather alerts (if any)
def display_weather_alerts(data, translator, lang):
    if "alerts" in data:
        for alert in data['alerts']:
            event = translator.translate(alert['event'], dest=lang).text
            description = translator.translate(alert['description'], dest=lang).text
            st.warning(f"Alert: {event}\n{description}")
    else:
        st.info(translator.translate("No weather alerts available.", dest=lang).text)

# Function to convert coordinates to city name
def get_city_name(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((lat, lon), language='en')
    return location.address.split(",")[0]

# Function to translate text
def translate_text(text, dest_language):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# Function to create different types of charts
def create_chart(chart_type, forecast_df):
    if chart_type == "Line Chart":
        fig = px.line(forecast_df, x="DateTime", y="Temperature", title="Temperature Forecast")
    elif chart_type == "Bar Chart":
        fig = px.bar(forecast_df, x="DateTime", y="Temperature", title="Temperature Forecast")
    elif chart_type == "Area Chart":
        fig = px.area(forecast_df, x="DateTime", y="Temperature", title="Temperature Forecast")
    elif chart_type == "Heat Map":
        fig = px.density_heatmap(forecast_df, x="DateTime", y="Temperature", title="Temperature Heat Map")
    elif chart_type == "Scatter Plot":
        fig = px.scatter(forecast_df, x="DateTime", y="Temperature", title="Temperature Scatter Plot")
    elif chart_type == "Calendar View":
        fig = go.Figure(data=[go.Scatter(x=forecast_df["DateTime"], y=forecast_df["Temperature"], mode='markers')])
        fig.update_layout(title="Calendar View", xaxis_title="Date", yaxis_title="Temperature")
    elif chart_type == "3D Surface Plot":
        fig = go.Figure(data=[go.Surface(z=forecast_df["Temperature"].values.reshape((5, 5)), colorscale='Viridis')])
        fig.update_layout(title="3D Surface Plot", scene=dict(zaxis_title="Temperature"))
    else:
        fig = px.line(forecast_df, x="DateTime", y="Temperature", title="Temperature Forecast")
    return fig

# Sidebar for location search and settings
st.sidebar.header("Settings")
country = st.sidebar.selectbox("Select Country", list(country_data.keys()))
state = st.sidebar.selectbox("Select State/Province", list(country_data[country].keys()))
city = st.sidebar.selectbox("Select City", country_data[country][state])

units = st.sidebar.radio("Select Temperature Unit", ("Celsius", "Fahrenheit"))
units = "imperial" if units == "Fahrenheit" else "metric"

# Language translation settings
st.sidebar.header("Language Translation")
languages = ['en', 'es', 'fr', 'de', 'ur', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi', 'bn', 'pa', 'jv', 'sw', 'vi', 'tr', 'pl', 'ro']
selected_language = st.sidebar.selectbox("Select Language", languages, format_func=lambda x: x.upper())

# Chart type selection
st.sidebar.header("Chart Type")
chart_type = st.sidebar.selectbox("Select Chart Type", [
    "Line Chart", "Bar Chart", "Area Chart", "Heat Map", "Scatter Plot", "Calendar View", "3D Surface Plot"])

translator = Translator()

# Main app interface
st.title("Weather Dashboard",)
st.markdown("## Current Weather and Forecast")

# Get current weather data
weather_data = get_weather_data(city, units)
if weather_data.get("cod") != 200:
    st.error(translator.translate(f"City {city} not found!", dest=selected_language).text)
else:
    # Display current weather
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(translator.translate(f"Weather in {city}", dest=selected_language).text)
        st.metric(translator.translate("Temperature", dest=selected_language).text, f"{weather_data['main']['temp']}°")
        st.text(translator.translate(f"Weather: {weather_data['weather'][0]['description'].title()}", dest=selected_language).text)
        st.text(translator.translate(f"Humidity: {weather_data['main']['humidity']}%", dest=selected_language).text)
        st.text(translator.translate(f"Wind Speed: {weather_data['wind']['speed']} m/s", dest=selected_language).text)
        
    with col2:
        st.subheader(translator.translate("Forecast", dest=selected_language).text)
        forecast_data = get_forecast_data(city, units)
        forecast_df = {
            "DateTime": [datetime.fromtimestamp(entry["dt"]) for entry in forecast_data["list"]],
            "Temperature": [entry["main"]["temp"] for entry in forecast_data["list"]],
            "Weather": [translator.translate(entry["weather"][0]["description"].title(), dest=selected_language).text for entry in forecast_data["list"]]
        }
        fig = create_chart(chart_type, forecast_df)
        st.plotly_chart(fig)

    # Display interactive weather map
    st.markdown(translator.translate("## Interactive Weather Map", dest=selected_language).text)
    lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]
    st.map(data={"lat": [lat], "lon": [lon]})

# Sidebar footer with additional features
st.sidebar.header(translator.translate("Additional Features", dest=selected_language).text)
if st.sidebar.button(translator.translate("View Weather Alerts", dest=selected_language).text):
    display_weather_alerts(weather_data, translator, selected_language)
