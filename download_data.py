import requests
import os

url = (
    "https://raw.githubusercontent.com/owid/covid-19-data/"
    "master/public/data/owid-covid-data.csv"
)

print("Downloading OWID COVID data...")
response = requests.get(url, timeout=60)
response.raise_for_status()

os.makedirs("data", exist_ok=True)
filepath = "data/owid-covid-data.csv"

with open(filepath, "wb") as f:
    f.write(response.content)

size_mb = round(os.path.getsize(filepath) / 1e6, 1)
print(f"Done! Saved to {filepath} ({size_mb} MB)")
