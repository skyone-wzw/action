import json
import time

import scrapy

import setting
from action.items import PictureItem


class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    allowed_domains = ['pixiv.net']
    start_urls = ['https://www.pixiv.net/']
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77',
            'Referer': "https://www.pixiv.net/"
        }
    }

    def parse(self, response, **kwargs):
        for index in range(1, 11):
            yield scrapy.Request(
                'https://www.pixiv.net/ajax/search/'
                '%s/%s?p=%d&lang=zh' % (setting.PIXIV_TYPE, setting.PIXIV_KEYWORD, index),
                callback=self.picture_info,
                dont_filter=True
            )
            time.sleep(setting.PIXIV_SLEEP_TIME)

    def picture_info(self, response, **kwargs):
        date = time.localtime()
        date = "%04d-%02d-%02d" % (date.tm_year, date.tm_mon, date.tm_mday - 1)
        data = json.loads(response.text)
        for item in data["body"]["illust"]["data"]:
            if date not in item["updateDate"]:
                for i in range(item["pageCount"]):
                    img = PictureItem()
                    img["path"] = "pixiv"
                    img["id"] = item["id"]
                    img["url"] = "https://i.pximg.net/img-original/img" + item["url"].split("img")[-1].split("_")[0]
                    img["title"] = item["title"]
                    img["author"] = item["userName"]
                    img["uid"] = item["userId"]
                    img["extension"] = img["url"].split('.')[-1]
                    img["name"] = ("%s_p%d-%s." % (img["id"], i, img["uid"])) + img["extension"]

                    img["url"] = img["url"] + ("p%d." % i) + img["extension"]
                    img["headers"] = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77',
                        'Referer': "https://www.pixiv.net/"
                    }
                    yield img
                    time.sleep(setting.PIXIV_SLEEP_TIME)
