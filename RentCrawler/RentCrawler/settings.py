# -*- coding: utf-8 -*-

# Scrapy settings for RentScrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
BOT_NAME = 'RentCrawler'
SPIDER_MODULES = ['RentCrawler.spiders']
NEWSPIDER_MODULE = 'RentCrawler.spiders'

ITEM_PIPELINES = {
    'RentCrawler.itempipelines.dataset_pipeline.DatasetPipeline': 300
}

SQLITE_URI='sqlite:///rent_crawler.db'
SQLITE_DATABASE='Rent'

# User settings
USER_AGENT = 'weitang114'
MAIL_FROM = 'rentcrawler@gmail.com'
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USER = 'rentcrawler@gmail.com'
MAIL_PASS = ''


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'RentScrawler (+http://www.yourdomain.com)'
