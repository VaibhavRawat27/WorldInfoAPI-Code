from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import requests
import pycountry
import random
import time

# ✅ Import static dictionaries
from dataset.data_store import (
    CULTURAL_NOTES, LANGUAGES, CURRENCIES, TIME_FUN_FACTS,
    HOLIDAYS, WHAT_HAPPENING_TODAY, COUNTRY_COORDS
)

app = Flask(__name__)

# ========================
# 🔹 CONFIG
# ========================
OPENWEATHER_API = "Your OpenWeatherAPI Key"
NASA_API = "Your NASA API Key"

# ✅ Simple In-Memory Cache
cache = {}
def set_cache(key, data, ttl=600):  # default 10 minutes
    cache[key] = {"data": data, "expires": time.time() + ttl}

def get_cache(key):
    if key in cache and cache[key]["expires"] > time.time():
        return cache[key]["data"]
    return None

# ========================
# 🔹 HELPER FUNCTIONS
# ========================

def get_country_from_timezone(tz_name):
    try:
        for country_code, timezones in pytz.country_timezones.items():
            if tz_name in timezones:
                return pycountry.countries.get(alpha_2=country_code).name
        return "Unknown"
    except:
        return "Unknown"

def get_greeting(hour):
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

def working_hours_status(hour):
    if 9 <= hour < 18:
        return "Office Hours"
    elif hour < 9:
        return "Early Morning"
    elif 18 <= hour < 21:
        return "After Hours"
    else:
        return "Late Night"

def get_moon_phase(date):
    diff = datetime.strptime(date, "%Y-%m-%d") - datetime(2001, 1, 1)
    days = diff.days + (diff.seconds / 86400)
    lunations = 0.20439731 + (days * 0.03386319269)
    phase_index = int((lunations % 1) * 8 + 0.5) % 8
    phases = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
              "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
    return phases[phase_index]

def get_sunrise_sunset(lat, lon, local_tz):
    cache_key = f"sun_{lat}_{lon}"
    cached = get_cache(cache_key)
    if cached: return cached

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API}")
        data = r.json()
        sunrise_utc = datetime.fromtimestamp(data['sys']['sunrise'], pytz.UTC)
        sunset_utc = datetime.fromtimestamp(data['sys']['sunset'], pytz.UTC)

        sunrise_local = sunrise_utc.astimezone(pytz.timezone(local_tz))
        sunset_local = sunset_utc.astimezone(pytz.timezone(local_tz))
        now_local = datetime.now(pytz.timezone(local_tz))

        is_day = sunrise_local <= now_local <= sunset_local
        result = (sunrise_local.strftime("%H:%M"), sunset_local.strftime("%H:%M"), is_day)
        set_cache(cache_key, result, 600)
        return result
    except:
        return "06:00", "18:30", True

def get_weather(lat, lon):
    cache_key = f"weather_{lat}_{lon}"
    cached = get_cache(cache_key)
    if cached: return cached

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API}")
        w = r.json()
        result = {
            "temperature": f"{round(w['main']['temp'],1)}°C",
            "condition": w['weather'][0]['description'].title(),
            "humidity": f"{w['main']['humidity']}%",
            "wind_speed": f"{w['wind']['speed']} m/s"
        }
        set_cache(cache_key, result, 600)
        return result
    except:
        return {
            "temperature": "27°C",
            "condition": "Clear Sky",
            "humidity": "60%",
            "wind_speed": "2 m/s"
        }

def get_nasa_image():
    cached = get_cache("nasa_image")
    if cached: return cached

    try:
        r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API}")
        data = r.json()
        result = {
            "title": data.get("title", "N/A"),
            "image_url": data.get("url", ""),
            "description": data.get("explanation", "")
        }
        set_cache("nasa_image", result, 86400)  # Cache for 24 hours
        return result
    except:
        return {
            "title": "Earth View",
            "image_url": "https://apod.nasa.gov/apod/image/1901/IC405_Abolfath_3952.jpg",
            "description": "Default NASA image fallback."
        }

def get_country_flag(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return f"https://flagcdn.com/w320/{country.alpha_2.lower()}.png"
    except:
        return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

def get_country_image(country_name):
    cached = get_cache(f"img_{country_name}")
    if cached: return cached

    try:
        r = requests.get(f"https://source.unsplash.com/600x400/?{country_name}")
        set_cache(f"img_{country_name}", r.url, 86400)
        return r.url
    except:
        return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

# ========================
# 🔹 MAIN API ROUTE
# ========================
@app.route('/time', methods=['GET'])
def get_time():
    tz_name = request.args.get("timezone")
    country_param = request.args.get("country")

    if country_param and not tz_name:
        for code, zones in pytz.country_timezones.items():
            if pycountry.countries.get(alpha_2=code).name == country_param:
                tz_name = zones[0]
                break

    if not tz_name:
        tz_name = "UTC"

    try:
        tz = pytz.timezone(tz_name)
    except:
        return jsonify({"error": "Invalid timezone. Example: Asia/Kolkata or use ?country=India"}), 400

    now = datetime.now(tz)
    hour = now.hour
    date_str = now.strftime("%Y-%m-%d")
    country = get_country_from_timezone(tz_name)

    lat, lon = COUNTRY_COORDS.get(country, (0, 0))
    sunrise, sunset, is_day = get_sunrise_sunset(lat, lon, tz_name)
    weather = get_weather(lat, lon)
    nasa_image = get_nasa_image()

    response = {
        "country": country,
        "flag_image": get_country_flag(country),
        "country_image": get_country_image(country),
        "date": date_str,
        "day": now.strftime("%A"),
        "time": now.strftime("%H:%M:%S"),
        "utc_offset": now.strftime("%z"),
        "greeting": get_greeting(hour),
        "working_hours_status": working_hours_status(hour),
        "public_holiday_today": HOLIDAYS.get(country, {}).get(now.strftime("%m-%d"), "No Holiday Today"),
        "is_daytime": is_day,
        "sunrise": sunrise,
        "sunset": sunset,
        "moon_phase": get_moon_phase(date_str),
        "weather": weather,
        "nasa_image": nasa_image,
        "language": LANGUAGES.get(country, "English"),
        "currency": CURRENCIES.get(country, {"name": "Unknown", "code": "N/A"}),
        "cultural_note": CULTURAL_NOTES.get(country, "No cultural data available."),
        "whats_happening_today": WHAT_HAPPENING_TODAY.get(country, "Nothing special today"),
        "time_fun_fact": TIME_FUN_FACTS.get(country, "Time is always moving forward!")
    }

    return jsonify(response)

# ========================
# 🔹 TIME COMPARISON ROUTE
# ========================
@app.route('/compare', methods=['GET'])
def compare_timezones():
    tz1 = request.args.get("from")
    tz2 = request.args.get("to")
    if not tz1 or not tz2:
        return jsonify({"error": "Please provide ?from=Asia/Kolkata&to=America/New_York"}), 400

    try:
        t1 = datetime.now(pytz.timezone(tz1))
        t2 = datetime.now(pytz.timezone(tz2))
        diff = abs((t1 - t2).total_seconds()) / 3600
        return jsonify({
            "from": tz1,
            "to": tz2,
            "time_now_from": t1.strftime("%H:%M:%S"),
            "time_now_to": t2.strftime("%H:%M:%S"),
            "difference_hours": round(diff, 2)
        })
    except:
        return jsonify({"error": "Invalid timezone names"}), 400

if __name__ == '__main__':
    app.run(debug=True)
