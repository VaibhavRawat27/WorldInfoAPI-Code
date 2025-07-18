# 🌍 WorldInfoAPI

WorldInfoAPI is a REST API that provides **real-time global information** – time, weather, sunrise/sunset, moon phases, cultural notes, NASA's Astronomy Picture of the Day, country flag, and more.

---

## 📖 Table of Contents

- [For Users](#-for-users)
  - [Base URL](#base-url)
  - [Quick Usage](#quick-usage)
  - [Examples](#examples)
- [API Endpoints](#-api-endpoints)
  - [/time](#1-time)
  - [/compare](#2-compare)
- [For Developers](#-for-developers)
  - [Folder Structure](#folder-structure)
  - [Run Locally](#run-locally)
  - [Editing Data Templates](#editing-data-templates)
- [Contributing](#-contributing)
- [Author](#-author)

---

## ✅ **For Users**

### Base URL

```
https://worldinfoapi.onrender.com
```

### Quick Usage

✅ **Check by Country**  
```
/time?country=India
```

✅ **Check by Timezone**  
```
/time?timezone=Asia/Kolkata
```

✅ **Compare Two Timezones**  
```
/compare?from=Asia/Kolkata&to=America/New_York
```

---

### Examples

**Check Current Time in India**  
👉 [https://worldinfoapi.onrender.com/time?country=India](https://worldinfoapi.onrender.com/time?country=India)

**Compare India and USA Time**  
👉 [https://worldinfoapi.onrender.com/compare?from=Asia/Kolkata&to=America/New_York](https://worldinfoapi.onrender.com/compare?from=Asia/Kolkata&to=America/New_York)

---

## ✅ **API Endpoints**

### 1) `/time`

Returns **real-time information** about the given country or timezone.

#### Parameters

| Name       | Type   | Required | Example             |
|------------|--------|----------|---------------------|
| `country`  | string | optional | `?country=India`    |
| `timezone` | string | optional | `?timezone=Asia/Kolkata` |

#### Sample Response

```json
{
  "country": "Australia",
  "country_image": "https://source.unsplash.com/600x400/?Australia",
  "cultural_note": "Casual 'G'day' with handshake.",
  "currency": {
    "code": "AUD",
    "name": "Australian Dollar"
  },
  "date": "2025-07-18",
  "day": "Friday",
  "flag_image": "https://flagcdn.com/w320/au.png",
  "greeting": "Good Night",
  "is_daytime": false,
  "language": "English",
  "moon_phase": "Last Quarter",
  "nasa_image": {
    "description": "Bright planet Saturn rises in evening skies...",
    "image_url": "https://apod.nasa.gov/apod/image/2507/ISSMeetsSaturn3_1024.jpg",
    "title": "ISS Meets Saturn"
  },
  "public_holiday_today": "No Holiday Today",
  "sunrise": "08:18",
  "sunset": "19:03",
  "time": "21:50:00",
  "time_fun_fact": "Australia has multiple time zones.",
  "utc_offset": "+1030",
  "weather": {
    "condition": "Clear Sky",
    "humidity": "40%",
    "temperature": "11.7°C",
    "wind_speed": "3.55 m/s"
  },
  "whats_happening_today": "Sydney Festival is ongoing.",
  "working_hours_status": "Late Night"
}
```

---

### 2) `/compare`

Compare time between two timezones.

```
/compare?from=Asia/Kolkata&to=America/New_York
```

#### Sample Response

```json
{
  "from": "Asia/Kolkata",
  "to": "America/New_York",
  "time_now_from": "20:11:25",
  "time_now_to": "10:41:25",
  "difference_hours": 9.5
}
```

---

## ✅ **For Developers**

### Folder Structure

```
WorldInfoAPI/
│
├── app.py                # Main Flask App
├── requirements.txt      # Required packages
├── dataset/
│   ├── data_store.py     # Static cultural data, currencies, etc.
│
└── README.md             # Documentation
```

---

### Run Locally

1. **Clone the repo:**

```bash
git clone https://github.com/YOUR_USERNAME/WorldInfoAPI.git
cd WorldInfoAPI
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the API:**

```bash
python app.py
```

4. **Open in browser:**

```
http://127.0.0.1:5000/time?country=India
```

---

### Editing Data Templates

You can update cultural facts, currencies, or fun facts by editing:

```
dataset/data_store.py
```

Example:

```python
CULTURAL_NOTES["Brazil"] = "Brazilians greet with a handshake or a kiss."
LANGUAGES["Brazil"] = "Portuguese"
CURRENCIES["Brazil"] = {"name": "Brazilian Real", "code": "BRL"}
```

Restart the server after making changes.

---

## ✅ **Contributing**

1. Fork the repo  
2. Create a new branch: `git checkout -b feature-name`  
3. Make your changes  
4. Submit a Pull Request

---

## 👨‍💻 **Author**

Developed by **Vaibhav Rawat**  
🔗 GitHub: [vaibhavrawat27](https://github.com/vaibhavrawat27)

---

### ⭐ **Support**

If you like this project, please **star ⭐ the repository** on GitHub!
