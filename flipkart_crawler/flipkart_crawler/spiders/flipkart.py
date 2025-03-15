import scrapy


class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com"]

    def parse(self, response):
        pass
