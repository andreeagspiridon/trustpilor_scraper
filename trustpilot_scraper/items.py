# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags



class TrustpilotScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    trust_score = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    location = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    services = scrapy.Field(input_processor = MapCompose(remove_tags))
