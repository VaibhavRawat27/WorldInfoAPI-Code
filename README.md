# 🌍 WorldInfoAPI

WorldInfoAPI is a REST API that provides **real-time global information** – time, weather, sunrise/sunset, moon phases, cultural notes, NASA's Astronomy Picture of the Day, country flag, and more.

---

## 📖 Documentation

- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Contributing](#contributing)

---

## ✅ Getting Started

### Base URL

```
https://worldinfoapi.onrender.com
```

### How to Use

#### By Country
```
/time?country=India
```

#### By Timezone
```
/time?timezone=Asia/Kolkata
```

#### Compare Two Timezones
```
/compare?from=Asia/Kolkata&to=America/New_York
```

---

## ✅ API Endpoints

### 1. `/time`

Returns **real-time information** about the given country or timezone.

#### Parameters

| Name       | Type   | Required | Example             |
|------------|--------|----------|---------------------|
| `country`  | string | optional | `?country=India`    |
| `timezone` | string | optional | `?timezone=Asia/Kolkata` |

#### Sample Response

```json
{
  "country": "India",
  "flag_image": "https://flagcdn.com/w320/in.png",
  "time": "20:11:25",
  "date": "2025-07-17",
  "weather": {
    "temperature": "27.7°C",
    "condition": "Overcast Clouds"
  },
  "nasa_image": {
    "title": "3I/ATLAS",
    "image_url": "https://apod.nasa.gov/apod/image/2507/noirlab2522a_3i1056.jpg"
  }
}
```

---

### 2. `/compare`

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

## ✅ Examples

### Check Current Time in India
```
https://worldinfoapi.onrender.com/time?country=India
```

### Compare India and USA Time
```
https://worldinfoapi.onrender.com/compare?from=Asia/Kolkata&to=America/New_York
```

### Example in Python

```python
import requests

res = requests.get("https://worldinfoapi.onrender.com/time?country=France")
print(res.json())
```

---

## ✅ Contributing

1. Fork the repo  
2. Make changes  
3. Submit a pull request

---

### ⭐ Support

If you like this project, **star ⭐ the repo**!

---

### 👨‍💻 Author

Developed by **Your Name**  
GitHub: [Your Profile](https://github.com/yourusername)
