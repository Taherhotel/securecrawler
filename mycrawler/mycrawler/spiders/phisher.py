import scrapy
from scrapy_playwright.page import PageMethod
import hashlib
from pathlib import Path
from pymongo import MongoClient

class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ["bmncollege.com"]
    start_urls = ["https://www.bmncollege.com/"]
    visited_urls = set()

    # ✅ Set up MongoDB connection
    client = MongoClient('localhost', 27018)
    db = client['phishing_data']  # Database name
    collection = db['scraped_sites']  # Collection name

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_page_coroutines': [
                        PageMethod('wait_for_load_state', 'domcontentloaded')
                    ]
                }
            )

    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.add(response.url)

            # Save HTML, title, and content to MongoDB
            title = response.css('title::text').get()
            content = response.text
            file_name = hashlib.md5(response.url.encode()).hexdigest() + ".html"

            # Save to file
            folder_path = Path.cwd() / 'data'
            folder_path.mkdir(parents=True, exist_ok=True)
            file_path = folder_path / file_name
            file_path.write_bytes(response.body)

            # Save to MongoDB
            self.collection.insert_one({
                'url': response.url,
                'title': title,
                'content': content,
                'html': response.body.decode('utf-8')
            })
            self.logger.info(f"Saved {response.url} as {file_name}")

            # Follow links (only 2 links max)
            if len(self.visited_urls) < 3:
                for link in response.css('a::attr(href)').getall():
                    absolute_url = response.urljoin(link)
                    if absolute_url not in self.visited_urls:
                        yield scrapy.Request(
                            absolute_url,
                            callback=self.parse,
                            meta={
                                'playwright': True,
                                'playwright_page_coroutines': [
                                    PageMethod('wait_for_load_state', 'domcontentloaded')
                                ]
                            }
                        )