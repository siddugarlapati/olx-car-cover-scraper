import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# I'm using this URL to scrape car covers from OLX
url = "https://www.olx.in/items/q-car-cover"

# My browser details to avoid blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Fetch data from OLX
def get_olx_data():
    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()  # Check if request worked
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    except:
        print("Failed to get OLX page. Maybe the site is down?")
        return None

# Extract listing details
def get_listings(soup):
    if not soup:
        return []
    
    all_listings = soup.find_all("li", class_="_1DNjI")  # Found this class by inspecting OLX
    results = []

    for item in all_listings:
        # Get title
        title = item.find("span", class_="_2poNJ")
        if title:
            title = title.text.strip()
        else:
            title = "Not available"

        # Get price
        price = item.find("span", class_="_1zgtX")
        if price:
            price = price.text.strip()
        else:
            price = "N/A"

        # Get location
        location = item.find("span", class_="_2VQu4")
        if location:
            location = location.text.strip()
        else:
            location = "Unknown"

        # Get date
        date = item.find("span", class_="_2dpZQ")
        if date:
            date = date.text.strip()
        else:
            date = "No date"

        results.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "Date Posted": date
        })

    return results

# Save to CSV
def save_results(data):
    if not data:
        print("No data to save!")
        return

    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
    filename = f"olx_car_covers_{timestamp}.csv"

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Location", "Date Posted"])
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved results to {filename}")
    except:
        print("Couldn't save to CSV. Maybe file is open?")

# Run everything
if __name__ == "__main__":
    print("Starting OLX scraper...")
    soup = get_olx_data()
    listings = get_listings(soup)
    save_results(listings)
    print("Done!")