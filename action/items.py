import scrapy


class PictureItem(scrapy.Item):
    path = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    id = scrapy.Field()
    uid = scrapy.Field()
    extension = scrapy.Field()
    headers = scrapy.Field()
