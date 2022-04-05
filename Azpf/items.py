# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AzpfItem(scrapy.Item):
    name = scrapy.Field()
    coin = scrapy.Field()
    url = scrapy.Field()
    funds = scrapy.Field()
    twitter = scrapy.Field()
    category = scrapy.Field()
    stage = scrapy.Field()
    pass

