#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-22 21:40:52

import os
from scrapy import Spider, Request
from scrapy.conf import settings
from hpoi_scrapy.items import AlbumItem, ImageItem


class HpoiSpider(Spider):
    name = 'hpoi'
    max_page = settings['MAX_CRAWL']

    def start_requests(self):
        if not os.path.exists(os.path.join(os.getcwd(), settings['IMAGE_DIRECTORY'])):
            os.mkdir(settings['IMAGE_DIRECTORY'])

        qs = 'order=top&r18=-1&original=0&itemCategory=0&category=60001&page=%d'
        for p in range(1, self.max_page+1):
            url = 'http://hpoi.net/album/list?' + qs % p
            yield Request(url, method='GET', callback=self.parse_albums_list)

    def parse_albums_list(self, response):
        for link in response.css('.album-box-figure>a::attr(href)').extract():
            url = 'http://hpoi.net/' + link
            yield Request(url, callback=self.parse_album)

    def parse_album(self, response):
        title, author = response.css('title').re(r'相册:(.*?) by (.*?) \| Hpoi手办维基')
        table = response.css('table>tbody>tr>td:last-child')
        if len(table) == 4:
            date, pics, clicks, source = table.re(r'^<td>\s*(\S+)\s*</td>$')
        elif len(table) == 5:
            date, pics, clicks = table.re(r'^<td>\s*(\S+)\s*</td>$')
            source = table[-1].css('a:attr(href)').extract()[0]
        else:
            raise ValueError('items table contains not 4 or 5 rows')
        pics, clicks = int(pics), int(clicks)
        intro = ''
        blockquote = response.css('blockquote')
        if blockquote:
            items = response.xpath('//blockquote//text()|//blockquote//br').re(r'(\S+)')
            intro = ''.join(items).replace('<br>', '\n')

        aitem = AlbumItem()
        aitem['url'] = response.url
        aitem['title'] = title
        aitem['author'] = author
        aitem['date'] = date
        aitem['pics'] = pics
        aitem['clicks'] = clicks
        aitem['source'] = source
        aitem['intro'] = intro
        yield aitem

        for iurl in response.css('.av-masonry-image-container>img::attr(src)').extract():
            yield Request(iurl, callback=self.parse_image, meta={'aurl': response.url})

        times = pics // 18
        if times > 0:
            img_id = response.css('body>script:last-child').re(r'init\((\d+)\)')[0]
            qs ='items=18&action=gal&offset=%d'
            for i in range(1, times+1):
                qsi = qs % (18*i)
                url = 'http://hpoi.net/album/gallery/%s?%s' % (img_id, qsi)
                yield Request(url, callback=self.more_images, meta={'aurl': response.url})

    def more_images(self, response):
        for iurl in response.css('img::attr(src)').extract():
            yield Request(iurl, callback=self.parse_image, meta=response.meta)

    def parse_image(self, response):
        iitem = ImageItem()
        iitem['url'] = response.url
        iitem['name'] = response.url.split('/')[-1]
        iitem['album_url'] = response.meta.get('aurl')
        iitem['image_content'] = response.body
        return iitem
