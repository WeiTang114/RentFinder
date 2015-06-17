import dataset
from scrapy import log
from RentCrawler.itempipelines.notifiers.emailer import Emailer

class DatasetPipeline(object):

    def __init__(self, sqlite_uri, sqlite_dbname, settings):
        self.tablename = 'Rent'
        self.sqlite_uri = sqlite_uri
        self.sqlite_dbname = sqlite_dbname
        self.notifiers = [
            Emailer(['weitang114@gmail.com'], settings)
        ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_uri=crawler.settings.get('SQLITE_URI'),
            sqlite_dbname=crawler.settings.get('SQLITE_DATABASE', 'RentItem'),
            settings=crawler.settings
        )

    def open_spider(self, spider):
        self.db = dataset.connect(self.sqlite_uri)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        log.msg('DatasetPipeline:Processcing item ' + item['objectId'], level=log.INFO)
        collection_name = item.__class__.__name__
        table = self.db[collection_name]

        if table.count(objectId=item['objectId']) > 0:
            log.msg('Item ' + item['objectId'] + ' existed.', level=log.INFO)
            old_item = table.find_one(objectId=item['objectId'])
            self.notify_if_better(old_item, item)
            table.update(item, ['objectId'])
        else:
            log.msg('New item ' + item['objectId'] + '.', level=log.INFO)
            self.notify_new(item)
            table.insert(item)

        return item

    def notify_if_better(self, old_item, item):
        if old_item['price'] > item['price']:
            [n.notify_lowerprice(old_item, item) for n in self.notifiers]

    def notify_new(self, item):
        [n.notify_new(item) for n in self.notifiers]
