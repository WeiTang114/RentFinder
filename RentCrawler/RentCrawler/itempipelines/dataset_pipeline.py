import dataset
from scrapy.mail import MailSender
from scrapy import log

class DatasetPipeline(object):

    def __init__(self, sqlite_uri, sqlite_dbname, settings):
        self.tablename = 'Rent'
        self.sqlite_uri = sqlite_uri
        self.sqlite_dbname = sqlite_dbname
        self.mailer = MailSender.from_settings(settings)
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
            self.notify_lowerprice(old_item, item)

    def notify_new(self, item):
        self.notify(item, "New Rent", "new rent")
        log.msg('Notifying new item:' + item['objectId'])

    def notify_lowerprice(self, old_item, item):
        self.notify(item, "Lower price", str(old_item['price']) + " to " + str(item['price']))
        log.msg('Notifying lower price item:' + item['objectId'])

    def notify(self, item, title, msg):
        msg = msg + "\n\n"  \
              + "Title:" + item["title"].encode("utf-8") \
              + "\nPrice:" + str(item["price"]) \
              + "\nAddress:" + item["address"].encode("utf-8") \
              + "\nFloor:" + item["floor"].encode("utf-8") \
              + "\nlink:" + item["link"].encode("utf-8") \
              + "\nID:" + item['objectId'].encode("utf-8")
        mail_to = ["weitang114@gmail.com"]
        self.mailer.send(to=mail_to, subject='Test ' + title, body=msg)
        log.msg('Sent mail notification to ' + str(mail_to) + '.')



