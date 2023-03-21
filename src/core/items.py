""" Scrapy items """

import scrapy


class CourseItem(scrapy.Item):
    """ The course item """

    url = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    publication_date = scrapy.Field()
    tags = scrapy.Field()

