
import os, re, json, urllib.request, datetime

API = "https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={key}"
key = os.environ["OWM_API_KEY"]
city = os.environ.get("CITY", "Istanbul")
country = os.environ.get("COUNTRY", "TR")

url = API.format(city=city, country=country, key=key)
with urllib.request.urlopen(url) as resp:
    data = json.loads(resp.read().decode("utf-8"))

temp = round(data["main"]["temp"])
desc = data["weather"][0]["description"].title()
sunrise = datetime.datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
sunset  = datetime.datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

weather_line = f"**{temp}°C**, _{desc}_ — Güneş: **{sunrise}** / **{sunset}** (UTC)"
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

readme = re.sub(r"<!-- WEATHER:START -->(.*?)<!-- WEATHER:END -->",
                f"<!-- WEATHER:START -->
{weather_line}
<!-- WEATHER:END -->",
                readme, flags=re.S)

readme = re.sub(r"<!--REFRESH_TIMESTAMP-->.*",
                f"<!--REFRESH_TIMESTAMP-->{timestamp}",
                readme)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
