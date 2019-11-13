# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from actor_scrape.items import ActorScrapeItem


class ActorSpider(scrapy.Spider):
    name = 'actor'
    allowed_domains = ['']
    start_urls = ["https://www.google.com/"]

    def parse(self, response):
        yield Request(url="https://bilutv.org/list-dien-vien",
                      callback=self.parsing_pages,
                      dont_filter=True)
        # return Request(url="https://bilutv.org/dien-vien/cuc-tinh-y-5948.html",
        #               callback=self.extract_actor,
        #               dont_filter=True)

    def parsing_pages(self, response):
        ls = []
        for i in range(2, 4, 1):
            ls.append('/list-dien-vien/trang-{}.html'.format(i))
        for i in ls:
            yield Request(url='https://bilutv.org' + i,
                          callback=self.page_info,
                          dont_filter=True)

    def page_info(self, response):
        body = response.xpath('//*[@class="block-film"][2]/ul')
        for info in body.xpath('li[2]'):
            url = info.xpath('div/a/@href').extract_first()
            yield Request(url='https://bilutv.org' + url, callback=self.extract_actor, dont_filter=True)

    def extract_actor(self, response):
        body = response.xpath('//*[@class="actor"]')
        left = body.xpath('//*[@class="l"]/div/@style').extract_first()
        right = body.xpath('//*[@class="r"]/div/text()').extract_first()
        loader = ItemLoader(item=ActorScrapeItem())
        loader.add_value('info', right)
        loader.add_value('img_url', left)

        return loader.load_item()
