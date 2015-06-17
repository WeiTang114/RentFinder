# coding=utf-8
from notifier import BaseNotifier
from scrapy import log
from scrapy.mail import MailSender

class Emailer(BaseNotifier):

    def __init__(self, receivers, settings):
        self.receivers = receivers
        self.mailer = MailSender.from_settings(settings)

    def notify_new(self, rentitem):
        subject = "[NewRent][" + str(rentitem['price']) + '] ' + rentitem['title']
        msg = "new rent"
        self.notify(rentitem, subject=subject, msg=msg)
        log.msg('Notifying new item:' + rentitem['objectId'])

    def notify_lowerprice(self, old_rentitem, rentitem):
        subject = "[Lower price][" + str(rentitem['price']) + '] ' + rentitem['title']
        msg = str(old_rentitem['price']) + " to " + str(rentitem['price'])
        self.notify(rentitem, subject=subject, msg=msg)
        log.msg('Notifying lower price item:' + rentitem['objectId'])

    def notify(self, rentitem, subject, msg):
        maplink = 'http://maps.google.com/?q=' + rentitem['address'].encode('utf-8')
        itemlink = rentitem['link'].encode('utf-8')
        NL = '<br>'
        msg = msg + NL \
              + 'Title:' + rentitem['title'].encode('utf-8') + NL \
              + 'Price:' + str(rentitem['price']) + NL \
              + 'Address:' + rentitem['address'].encode('utf-8') + ' ' \
              + '<a href="' + maplink + '">' + 'Google Map' + '</a>' + NL \
              + 'Floor:' + rentitem['floor'].encode('utf-8') + NL \
              + 'Link:' + NL \
              + '<a href="' + itemlink + '">' + itemlink + '</a>' + NL \
              + 'ID:' + rentitem['objectId'].encode('utf-8')

        self.mailer.send(to=self.receivers, subject=subject, body=msg, mimetype='text/html')
        log.msg('Sent mail notification to ' + str(self.receivers) + '.')

