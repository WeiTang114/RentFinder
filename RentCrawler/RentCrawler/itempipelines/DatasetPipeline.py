import dataset
from scrapy.mail import MailSender

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
        print 'DatasetPipeline:Processcing item ', item['objectId']
        collection_name = item.__class__.__name__

        table = self.db[collection_name]
        print item['objectId']

        if table.count(objectId=item['objectId']) > 0:
            old_item = table.find_one(objectId=item['objectId'])
            self.notify_if_better(old_item, item)
            table.update(item, ['objectId'])
        else:
            self.notify_new(item)
            table.insert(item)

        print table.count()
        return item


    def notify_if_better(self, old_item, item):
        if old_item['price'] > item['price']:
            self.notify_lowerprice(old_item, item)

    def notify_new(self, item):
        self.notify(item, "New Rent", "new rent")

    def notify_lowerprice(self, old_item, item):
        self.notify(item, "Lower price", str(old_item['price']) + " to " + str(item['price']))

    def notify(self, item, title, msg):
        msg = msg + "\n\n"  \
              + "Title:" + item["title"].encode("utf-8") \
              + "\nPrice:" + str(item["price"]) \
              + "\nAddress:" + item["address"].encode("utf-8") \
              + "\nFloor:" + item["floor"].encode("utf-8") \
              + "\nlink:" + item["link"].encode("utf-8") \
              + "\nID:" + item['objectId'].encode("utf-8")
        self.mailer.send(to=["weitang114@gmail.com"], subject=title, body=msg)



