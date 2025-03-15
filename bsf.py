from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
url="https://amazon.ca"
r=requests.get(url)

#print(r.text)

with open("file.html",'w') as f :
    f.write(r.text)
with open("file.html","r") as f:
    html = f.read()

soup = BeautifulSoup(html , 'html.parser')

#print(soup.prettify())
title = soup.title.text
print("Title:", title)

login_links = []
for link in soup.find_all("a", href=True):
    href = link["href"]
    if "login" in href or "signin" in href:
        login_links.append(href)

print("Login Links:", login_links)

login_forms = []
for form in soup.find_all("form"):
    form_data = {
        "action": form.get("action"),  
        "method": form.get("method"), 
        "inputs": [inp.get("name") for inp in form.find_all("input")]
    }
    login_forms.append(form_data)

print("Login Forms:", login_forms)


client = MongoClient("mongodb://localhost:27018/")

db = client["phishing_data"]

collection = db["scraped_sites"]
data = {
    "url": url,
    "title": title,
    "login_links": login_links,
    "login_forms": login_forms
}

collection.insert_one(data)
print("Data saved to MongoDB!")
