from pymongo import MongoClient

# Connect to local MongoDB instance
client = MongoClient("mongodb://localhost:27018/")

# Create a database (if it doesn't exist)
db = client["phishing_data"]

# Create a collection (like a table)
collection = db["scraped_sites"]

data = {
    "url": "https://example.com",
    "title": "Example Page",
    "content": "This is an example of scraped content."
}

collection.insert_one(data)  # Insert into the collection