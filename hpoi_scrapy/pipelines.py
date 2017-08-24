# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import io
import os
import sqlite3
from PIL import Image
from scrapy.conf import settings
from hpoi_scrapy.items import AlbumItem, ImageItem


class MainPipeline(object):
    db, cur = None, None
    insert_album = 'INSERT INTO album(url,title,author,date,pics,clicks,source,intro) VALUES(?,?,?,?,?,?,?,?);'
    insert_image = 'INSERT INTO image(url,name,album_url) VALUES(?,?,?);'
    def open_spider(self, spider):
        self.db = sqlite3.connect(settings['DB_NAME'])
        self.cur = self.db.cursor()
    def close_spider(self, spider):
        if self.db:
            self.db.commit()
        if self.cur:
            self.cur.close()
        if self.db:
            self.db.close()
    def process_item(self, item, spider):
        if isinstance(item, AlbumItem):
            t = (item['url'], item['title'], item['author'], item['date'], item['pics'], item['clicks'], item['source'], item['intro'])
            self.cur.execute(self.insert_album, t)
            spider.logger.info('processing album ' + t[1])
        if isinstance(item, ImageItem):
            content = item['image_content']
            img = Image.open(io.BytesIO(content))
            img.save(os.path.join(settings['IMAGE_DIRECTORY'], item['name']))
            t = (item['url'], item['name'], item['album_url'])
            self.cur.execute(self.insert_image, t)
            spider.logger.info('processing images in ' + t[2])
        return item


# Failed since database operations synchronization.
# import abc
# class BasePipeline(abc.ABC):
#     db, cur = None, None
#     def open_spider(self, spider):
#         self.db = sqlite3.connect('hpoi.sqlite')
#         self.cur = self.db.cursor()
#     def close_spider(self, spider):
#         if self.db:
#             self.db.commit()
#         if self.cur:
#             self.cur.close()
#         if self.db:
#             self.db.close()
#     @abc.abstractmethod
#     def process_item(self, item, spider):
#         ...
# class AlbumPipeline(BasePipeline):
#     insert_album = 'INSERT INTO album(url,title,author,date,pics,clicks,source,intro) VALUES(?,?,?,?,?,?,?,?);'
#     def process_item(self, item, spider):
#         if isinstance(item, AlbumItem):
#             t = (item['url'], item['title'], item['author'], item['date'], item['pics'], item['clicks'], item['source'], item['intro'])
#             self.cur.execute(self.insert_album, t)
#             spider.logger.info('processing album ' + t[1])
#         return item  # important, otherwise this item will lose
# class ImagePipeline(BasePipeline):
#     insert_image = 'INSERT INTO image(url,name,album_url) VALUES(?,?,?);'
#     def process_item(self, item, spider):
#         if isinstance(item, ImageItem):
#             content = item['image_content']
#             img = Image.open(io.BytesIO(content))
#             img.save(os.path.join(settings['IMAGE_DIRECTORY'], item['name']))
#             t = (item['url'], item['name'], item['album_url'])
#             self.cur.execute(self.insert_image, t)
#             spider.logger.info('processing images in ' + t[2])
#         return item
