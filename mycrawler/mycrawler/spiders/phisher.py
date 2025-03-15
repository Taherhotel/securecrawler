from pathlib import Path
import scrapy
import hashlib
from urllib.parse import urljoin

class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ["bmncollege.com"]
    start_urls = ["https://www.bmncollege.com/"]

    link_count = 0
    max_links = 2
    visited_urls = set()

    def start_requests(self):
        for url in self.start_urls:
            self.visited_urls.add(url)  # Mark start URL as visited
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Save the current page as HTML
        title = response.css('title::text').get()
        file_name = hashlib.md5(response.url.encode()).hexdigest() + ".html"
        
        folder_path = Path.cwd() / 'data'
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / file_name
        file_path.write_text(response.text, encoding='utf-8')

        self.logger.info(f"Saved {response.url} as {file_name}")

        yield {
            'url': response.url,
            'title': title
        }

        # ✅ Target the "Contact Us" link specifically
        contact_link = response.xpath("//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact us')]/@href").get()
        if contact_link and self.link_count < self.max_links:
            absolute_url = urljoin(response.url, contact_link.strip())
            if absolute_url.startswith('http') and absolute_url not in self.visited_urls:
                self.visited_urls.add(absolute_url)
                self.link_count += 1
                self.logger.info(f"Following 'Contact Us' link: {absolute_url}")
                yield scrapy.Request(absolute_url, callback=self.parse)