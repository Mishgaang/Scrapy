# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_currency(value):
    return value.replace('£', '').strip()


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(remove_tags), ouput_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags), ouput_processor=TakeFirst())
    link = scrapy.Field()
