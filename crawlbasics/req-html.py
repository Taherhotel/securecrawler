from requests_html import HTMLSession
from pymongo import MongoClient

# Create a session
session = HTMLSession()

# Target URL
url = "https://www.flipkart.com/audio-video/speakers/pr?sid=0pm%2C0o7&sort=popularity&param=8755&p%5B%5D=facets.rating%255B%255D%3D3%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=facets.price_range.from%3D599&p%5B%5D=facets.price_range.to%3DMax&p%5B%5D=facets.type%255B%255D%3DHome%2BAudio%2BSpeaker&p%5B%5D=facets.type%255B%255D%3DGaming%2BSpeaker&p%5B%5D=facets.type%255B%255D%3DHome%2BTheatre&p%5B%5D=facets.type%255B%255D%3DLaptop%252FDesktop%2BSpeaker&p%5B%5D=facets.type%255B%255D%3DMobile%252FTablet%2BSpeaker&p%5B%5D=facets.type%255B%255D%3DSoundbar&param=443&hpid=-9HuwFIVtikIZ8W21KTsvKp7_Hsxr70nj65vMAAFKlc%3D&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJGcm9tIOKCuTQ5OSoiXSwidmFsdWVUeXBlIjoiTVVMVElfVkFMVUVEIn19LCJoZXJvUGlkIjp7InNpbmdsZVZhbHVlQXR0cmlidXRlIjp7ImtleSI6Imhlcm9QaWQiLCJpbmZlcmVuY2VUeXBlIjoiUElEIiwidmFsdWUiOiJBQ0NIRlJIM0hFNEdDWlpGIiwidmFsdWVUeXBlIjoiU0lOR0xFX1ZBTFVFRCJ9fSwidGl0bGUiOnsibXVsdGlWYWx1ZWRBdHRyaWJ1dGUiOnsia2V5IjoidGl0bGUiLCJpbmZlcmVuY2VUeXBlIjoiVElUTEUiLCJ2YWx1ZXMiOlsiQmVzdCBTZWxsaW5nIE1vYmlsZSBTcGVha2VycyJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D"

# Get and render the page (Handles JavaScript)
response = session.get(url)
response.html.render(timeout=30)  # Increase timeout if needed

# Save HTML to file (optional)
with open("file.html", "w") as f:
    f.write(response.html.html)

# Extract Title
title = response.html.find("title", first=True).text
print("Title:", title)

# Extract Login Links
login_links = []
for link in response.html.find("a"):
    href = link.attrs.get("href", "")
    if "login" in href or "signin" in href:
        login_links.append(href)

print("Login Links:", login_links)

# Extract Login Forms
login_forms = []
for form in response.html.find("form"):
    form_data = {
        "action": form.attrs.get("action", ""),
        "method": form.attrs.get("method", ""),
        "inputs": [inp.attrs.get("name") for inp in form.find("input") if inp.attrs.get("name")]
    }
    login_forms.append(form_data)

print("Login Forms:", login_forms)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27018/")
db = client["phishing_data"]
collection = db["scraped_sites"]

# Save to MongoDB
data = {
    "url": url,
    "title": title,
    "login_links": login_links,
    "login_forms": login_forms
}

collection.insert_one(data)
print("Data saved to MongoDB!")