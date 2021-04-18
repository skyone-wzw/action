import json
import time

import scrapy

import setting
from action.items import PictureItem


class PictureSpider(scrapy.Spider):
    name = 'bili'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://h.bilibili.com/']

    def parse(self, response, **kwargs):
        for i in range(setting.BILI_MAX_PAGE):
            yield scrapy.Request(
                'https://api.vc.bilibili.com/link_draw/v2/Doc/list?page_size=20'
                '&type=' + setting.BILI_TYPE +
                '&category=' + setting.BILI_CATEGORY +
                '&page_num=' + str(i),
                callback=self.picture_info,
                dont_filter=True
            )

    def picture_info(self, response, **kwargs):
        data = json.loads(response.text)
        for item in data["data"]["items"]:
            img = PictureItem()
            img["path"] = "bili"
            img["url"] = item["item"]["pictures"][-1]["img_src"]
            img["title"] = item["item"]["title"]
            img["id"] = item["item"]["doc_id"]
            img["author"] = item["user"]["name"]
            img["uid"] = item["user"]["uid"]
            img["extension"] = img["url"].split('.')[-1]
            img["name"] = str(img["id"]) + '.' + img["extension"]
            img["headers"] = {}
            yield img
            time.sleep(setting.BILI_SLEEP_TIME)
