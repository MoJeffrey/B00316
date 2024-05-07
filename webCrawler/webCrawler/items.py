# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebcrawlerItem(scrapy.Item):
    before = scrapy.Field()
    now = scrapy.Field()
    show = scrapy.Field()
    matplotJudgment = scrapy.Field()