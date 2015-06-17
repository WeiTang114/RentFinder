from notifier import BaseNotifier
from scrapy import log
from scrapy.mail import MailSender

class Emailer(BaseNotifier):

    def __init__(self, receivers, settings):
        self.receivers = receivers
        self.mailer = MailSender.from_settings(settings)

    def notify_new(self, rentitem):
        title = "New Rent"
        msg = "new rent"
        self.notify(rentitem, title=title, msg=msg)
        log.msg('Notifying new item:' + rentitem['objectId'])

    def notify_lowerprice(self, old_rentitem, rentitem):
        title = "Lower price"
        msg = str(old_rentitem['price']) + " to " + str(rentitem['price'])
        self.notify(rentitem, title=title, msg=msg)
        log.msg('Notifying lower price item:' + rentitem['objectId'])

    def notify(self, rentitem, title, msg):
        msg = msg + "\n\n"  \
              + "Title:" + rentitem["title"].encode("utf-8") \
              + "\nPrice:" + str(rentitem["price"]) \
              + "\nAddress:" + rentitem["address"].encode("utf-8") \
              + "\nFloor:" + rentitem["floor"].encode("utf-8") \
              + "\nlink:\n" + rentitem["link"].encode("utf-8") \
              + "\nID:" + rentitem['objectId'].encode("utf-8")
        self.mailer.send(to=self.receivers, subject=title, body=msg)
        log.msg('Sent mail notification to ' + str(self.receivers) + '.')

