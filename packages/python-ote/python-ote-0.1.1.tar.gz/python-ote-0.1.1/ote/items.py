# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import time
import locale

import scrapy
from itemloaders.processors import TakeFirst


def parse_time(values):
    return [time(int(value) - 1) for value in values]


def parse_price(values):
    locale.setlocale(locale.LC_NUMERIC, 'cs_CZ.UTF-8')
    return [locale.atof(value.replace(' ', '')) for value in values]


class DayMarketPricesItem(scrapy.Item):
    date = scrapy.Field(output_processor=TakeFirst())
    time = scrapy.Field(input_processor=parse_time, output_processor=TakeFirst())
    price = scrapy.Field(input_processor=parse_price, output_processor=TakeFirst())
