import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

locations = ["Half Moon Bay, California", "Huntington Beach", "Providence, Rhode Island", "Wrightsville Beach, North Carolina"]
base_URL = "https://www.tide-forecast.com/locations/{location}/tides/latest"

def web_scraper():
	d = {}

	for location in locations:
		d[location] = []
		parsed_location = location.replace(",", "").replace(" ", "-")
		page = requests.get(base_URL.format(location=parsed_location))
		soup = BeautifulSoup(page.content, "html.parser")
		days = soup.find_all("div", "tide-day")
		for index, day in enumerate(days):
			if index == 0:
				date = day.text.split("(")[1].split(")")[0]
			else:
				date = day.text.split("(")[2].split(")")[0]
			sunrise = parse(day.text.split("Sunrise:")[1][:7].strip())
			sunset = parse(day.text.split("Sunset:")[1][:7].strip())

			tide_data = day.text.split("Low Tide")[1:]
			for tide in tide_data:
				tide_time = parse(tide[:8].strip())
				if sunrise < tide_time < sunset:
					height = tide.split(")")[1].split("(")[0].strip()
					d[location].append({date: [tide[:8].strip(), height]})
	return d

if __name__ == "__main__":
	data = web_scraper()
	for city, tide_info in data.items():
		print(city)
		for tide in tide_info:
			print("\t", tide)
