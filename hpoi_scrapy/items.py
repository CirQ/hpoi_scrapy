# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AlbumItem(Item):
    url = Field()
    title = Field()
    author = Field()
    date = Field()
    pics = Field()
    clicks = Field()
    source = Field()
    intro = Field()


class ImageItem(Item):
    url = Field()
    name = Field()
    album_url = Field()
    image_content = Field()
