from typing import List

import scrapy


class RentalItem(scrapy.Item):
    url: str = scrapy.Field()
    title: str = scrapy.Field()
    status: str = scrapy.Field()
    pictures: List[str] = scrapy.Field()
    rent_price: float = scrapy.Field()
    description: str = scrapy.Field()
    phone_number: str = scrapy.Field()
    email: str = scrapy.Field()
