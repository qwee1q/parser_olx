from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from curl_cffi import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://www.olx.ua"

@app.get("/")
def main():
    resp = requests.get(
        "https://www.olx.ua/uk/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/",
        impersonate="chrome",
        timeout=15,
    )
    if resp.status_code != 200:
        return {"status": resp.status_code}

    soup = BeautifulSoup(resp.text, "html.parser")
    blocks = soup.find_all("div", class_="css-ih6nf2")

    if blocks is None:
        return {"error": "div не знайдено", "html_len": len(resp.text)}

    items = []
    for b in blocks:
        link = b.select_one('a[data-testid="card-title-link"]')
        title = b.select_one("h4")
        price = b.select_one('p[data-testid="ad-price"]')
        state = b.select_one('div[class="css-16y676b"]')
        location_date = b.select_one('p[data-testid="location-date"]')
        items.append({
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "url": BASE_URL + link["href"] if link and link.get("href") else None,
            "state": state.get_text(strip=True) if state else None,
            "location_date": location_date.get_text(strip=True) if location_date else None,
        })

    return {"count": len(items), "items": items}
