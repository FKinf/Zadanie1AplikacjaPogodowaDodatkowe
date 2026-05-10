import logging
import os
import datetime
import requests
from flask import Flask, render_template, request

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Dane autora i konfiguracja
AUTHOR = "Filip Kwietniak"
PORT = int(os.environ.get("PORT", 8080))
API_KEY = os.environ.get("WEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Lista krajów i miast
LOCATIONS = {
    "Polska": ["Warszawa", "Kraków", "Gdańsk", "Wrocław", "Poznań", "Lublin"],
    "Wielka Brytania": ["London", "Manchester", "Birmingham", "Edinburgh", "Bristol"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
}

# Log uruchomienia — wymagany przez zadanie 
logger.info(f"=== Aplikacja uruchomiona ===")
logger.info(f"Data uruchomienia : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logger.info(f"Autor             : {AUTHOR}")
logger.info(f"Nasłuchuje na porcie TCP: {PORT}")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    selected_country = None
    selected_city = None

    if request.method == "POST":
        selected_country = request.form.get("country")
        selected_city = request.form.get("city")

        if selected_country and selected_city:
            try:
                response = requests.get(BASE_URL, params={
                    "q": selected_city,
                    "appid": API_KEY,
                    "units": "metric",
                    "lang": "pl"
                }, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "description": data["weather"][0]["description"].capitalize(),
                        "temp": round(data["main"]["temp"], 1),
                        "feels_like": round(data["main"]["feels_like"], 1),
                        "humidity": data["main"]["humidity"],
                        "wind": round(data["wind"]["speed"] * 3.6, 1),  
                        "pressure": data["main"]["pressure"],
                    }
                else:
                    error = f"Nie można pobrać pogody dla miasta: {selected_city}"
            except requests.exceptions.Timeout:
                error = "Przekroczono czas połączenia z API pogodowym."
            except Exception as e:
                error = f"Błąd: {str(e)}"

    return render_template(
        "index.html",
        locations=LOCATIONS,
        weather=weather,
        error=error,
        selected_country=selected_country,
        selected_city=selected_city,
        author=AUTHOR,
    )

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
