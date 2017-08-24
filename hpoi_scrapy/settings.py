# -*- coding: utf-8 -*-

# Scrapy settings for hpoi_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hpoi_scrapy'

SPIDER_MODULES = ['hpoi_scrapy.spiders']
NEWSPIDER_MODULE = 'hpoi_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hpoi_scrapy (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# ITEM_PIPELINES = {
#     'hpoi_scrapy.pipelines.AlbumPipeline': 0,
#     'hpoi_scrapy.pipelines.ImagePipeline': 1
# }
ITEM_PIPELINES = {
    'hpoi_scrapy.pipelines.MainPipeline': 999
}

IMAGE_DIRECTORY = 'images/'
DB_NAME = 'hpoi.sqlite'
MAX_CRAWL = 1
