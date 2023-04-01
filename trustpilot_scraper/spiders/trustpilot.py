import scrapy
from scrapy import Request


class TrustpilotSpider(scrapy.Spider):
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }
    name = "trustpilot"
    allowed_domains = ["www.trustpilot.com"]
    start_urls = ["https://www.trustpilot.com/categories/personal_care?country=GB"]

    def parse(self, response):
        reviews = response.css('section.styles_feed__MNr87 > div.styles_wrapper__2JOo2')
        for review in reviews:
            title = review.css('p.styles_displayName__GOhL2::text').get()
            trust_score = review.css('span.styles_trustScore__8emxJ::text').getall()
            trust_score = [score.strip() for score in trust_score if score.strip()][0]
            location = review.css('span.styles_location__ILZb0::text').get()
            services = review.css('div.styles_categoriesLabels__FiWQ4 > span.typography_appearance-default__AAY17::text').getall()
            services = set(services)
            yield {
                'title': title,
                'trust_score':trust_score,
                'location': location,
                'services': services
            }
        try:
            next_page = response.css('[data-pagination-button-next-link="true"]').attrib['href']
        except KeyError:
            next_page = None
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)

