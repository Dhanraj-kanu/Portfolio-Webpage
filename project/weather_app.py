
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

API_KEY = "27a506cd7653c1bd7acd901f880fc46f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def configure_label(label, text, font, bg, fg):
    label.config(text=text, font=font, bg=bg, fg=fg, padx=10, pady=10)

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "City name cannot be empty!")
        return

    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        weather_data = response.json()
        if weather_data["cod"] != 200:
            raise ValueError("City not found")

        city_name, temp, humidity, wind_speed = weather_data["name"], weather_data["main"]["temp"], weather_data["main"]["humidity"], weather_data["wind"]["speed"]
        condition, icon_code = weather_data["weather"][0]["description"].capitalize(), weather_data["weather"][0]["icon"]
        rain_chance = weather_data.get("rain", {}).get("1h", 0)

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_photo = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw).resize((60, 60)))

        # Update UI
        weather_label.config(text=f"{city_name}: {temp}°C\n{condition}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        rain_label.config(text=f"Rain: {rain_chance} mm")
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        # Background and style changes
        root.config(bg="#FF4500" if temp > 30 else "#1E90FF" if temp >= 20 else "#4682B4")
        for label in [weather_label, humidity_label, wind_label]:
            configure_label(label, label.cget("text"), ("Arial", 18 if label == weather_label else 14, "bold"), "#4682B4", "white")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather: {e}")

def show_rain():
    rain_label.config(text=f"Rain Chance: {random.randint(0, 100)}%")

# UI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("450x550")
root.resizable(False, False)

bg_label = tk.Label(root, bg="#87CEEB", width=450, height=550)
bg_label.place(relwidth=1, relheight=1)

header = tk.Label(root, text="Weather App", font=("Arial", 25, "bold"), bg="#FFCC00", fg="black", relief="raised", bd=5)
header.pack(fill="x")

city_entry = tk.Entry(root, font=("Arial", 16), width=20, justify="center", bd=5, relief="sunken")
city_entry.pack(pady=30)

search_button = tk.Button(root, text="Get Weather", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=3, command=get_weather)
search_button.pack(pady=10)

rain_button = tk.Button(root, text="Show Rain", font=("Arial", 14, "bold"), bg="#FF6347", fg="white", relief="raised", bd=3, command=show_rain)
rain_button.pack(pady=10)

# Labels for weather data
weather_label, humidity_label, wind_label, rain_label = [tk.Label(root, font=("Arial", 14), relief="solid", bd=2) for _ in range(4)]
weather_label.pack(pady=20)
humidity_label.pack()
wind_label.pack()
rain_label.pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack(pady=10)

root.mainloop()
