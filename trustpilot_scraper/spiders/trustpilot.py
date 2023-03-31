import scrapy


class TrustpilotSpider(scrapy.Spider):
    name = "trustpilot"
    allowed_domains = ["www.trustpilot.com"]
    start_urls = ["http://www.trustpilot.com/"]

    def parse(self, response):
        pass
