import scrapy
from scrapy import Request
from trustpilot_scraper.items import TrustpilotScraperItem
from scrapy.loader import ItemLoader


class TrustpilotSpider(scrapy.Spider):
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'HTTPCACHE_ENABLED': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [503, 502, 501, 302, 301, 403, 404, 402, 401, 400, 500],
        'DOWNLOAD_DELAY': 1.5
    }
    name = "trustpilot"
    allowed_domains = ["uk.trustpilot.com"]
    start_urls = ["https://uk.trustpilot.com/categories"]

    headers = {
        'authority': 'uk.trustpilot.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.7',
        'cache-control': 'max-age=0',
        'if-none-match': '"euzidjsu36a31l"',
        'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    def parse(self, response, **kwargs):
        categories = response.css('div.styles_list__jB_Xe a::attr(href)').getall()
        categories = set(categories)
        for category in categories:
            category_url = response.urljoin(category)
            yield Request(category_url, callback=self.parse_reviews, dont_filter=True,
                          headers=self.headers)

    def parse_reviews(self, response):
        reviews = response.css('section.styles_feed__MNr87 > div.styles_wrapper__2JOo2')
        for review in reviews:
            l = ItemLoader(item=TrustpilotScraperItem(), selector=review)
            title = review.css('p.styles_displayName__GOhL2::text').get()
            l.add_value('title', title)

            trust_score = review.css('span.styles_trustScore__8emxJ::text').getall()
            try:
                trust_score = [score.strip() for score in trust_score if score.strip()][0]
            except IndexError:
                trust_score = 'N/A'
            l.add_value('trust_score', trust_score)

            location = review.css('span.styles_location__ILZb0::text').get()
            if not location:
                location = 'N/A'
            l.add_value('location', location)

            services = review.css('div.styles_categoriesLabels__FiWQ4 > '
                                  'span.typography_appearance-default__AAY17::text').getall()
            services = list(set(services))
            l.add_value('services', services)
            yield l.load_item()
        try:
            next_page = response.css('[data-pagination-button-next-link="true"]').attrib['href']
        except KeyError:
            next_page = None
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse_reviews, headers=self.headers)
