import requests
from os import path


class DownloadPipeline:
    def process_item(self, item, spider):
        name = str(item["name"])
        res = requests.get(item["url"], headers=item["headers"])
        if "404" in res.text:
            item["name"] = item["name"][:-3] + "png"
            item["url"] = item["url"][:-3] + "png"
            res = requests.get(item["url"], headers=item["headers"])
        with open(path.join(path.join(path.abspath('.'), item["path"]), name), 'wb') as file:
            file.write(res.content)
            print(item["title"])
        return item
