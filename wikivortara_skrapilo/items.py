# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikivortaraSkrapiloItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nomo = scrapy.Field()
    semantiko = scrapy.Field()
    morfologio = scrapy.Field()
    exemplaro = scrapy.Field()
    sinonimo = scrapy.Field()
    antonimo = scrapy.Field()
    angliana = scrapy.Field()
    franciana = scrapy.Field()
    germaniana = scrapy.Field()
    hispaniana = scrapy.Field()
    italiana = scrapy.Field()
    rusiana = scrapy.Field()
