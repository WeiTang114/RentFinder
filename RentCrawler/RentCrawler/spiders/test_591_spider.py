import scrapy
from scrapy.selector import Selector
import json
from RentCrawler.items import RentItem
import codecs
from scrapy import log

class Test591Spider(scrapy.spider.Spider):
    name = "test591"
    allowed_domains = ["rent.591.com.tw"]
    start_urls = [
        "http://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=3&listview=img&rentprice=3&section=37&pattern=2&order=posttime&orderType=desc"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-1]

        data = json.loads(response.body)
        main = data['main']

        #print main
        with codecs.open('out/' + filename, 'w', 'utf-8') as f:
            f.write(response.body.encode('utf-8'))

        rents_html = Selector(text=main, type="html").xpath("//div[@class='shList ']")
        log.msg("Crawled rents count: " + str(len(rents_html)), level=log.DEBUG)

        for rent_html in rents_html:
            item = RentItem()
            item['objectId'] = self.get_id(rent_html).decode("utf-8")
            item['title'] = self.get_title(rent_html).decode("utf-8")
            item['price'] = self.get_price(rent_html)
            item['address'] = self.get_address(rent_html).decode("utf-8")
            item['floor'] = self.get_floor(rent_html).decode("utf-8")
            item['link'] = self.get_link(rent_html).decode("utf-8")
            yield item

    def get_id(self, rent_html):
        objectId = rent_html.xpath(".//div[@class='left']/@data-bind")[0] \
            .extract() \
            .encode("utf-8")
        log.msg("id:" + objectId, level=log.DEBUG)
        return objectId

    def get_title(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        titlediv = datadiv.xpath(".//p[@class='title']//@title")
        title = titlediv[0].extract().encode('utf-8')
        log.msg(title, level=log.DEBUG)
        return title

    def get_price(self, rent_html):
        price_str = rent_html \
                    .xpath(".//li[@class='price fc-org']//strong[@class='']/text()") \
                    .extract()[0] \
                    .encode("utf-8")
        price_str = ''.join([s for s in price_str if s.isdigit()])
        price = int(price_str)

        log.msg(str(price), level=log.DEBUG)
        return price

    def get_address(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        addrp = datadiv.xpath("p")[1]
        addr = addrp.xpath("text()")[0].extract().encode("utf-8")
        log.msg(addr, level=log.DEBUG)
        return addr

    def get_floor(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        floorp = datadiv.xpath("p")[2]
        floor = ''.join(floorp.xpath(".//text()").extract()).encode("utf-8")
        log.msg(floor, level=log.DEBUG)
        return floor

    def get_datadiv(self, rent_html):
        datadiv = rent_html.xpath(".//div[@class='right']")[0]
        return datadiv

    def get_link(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        titlep = datadiv.xpath(".//p[@class='title']")
        href = titlep.xpath(".//@href")[0].extract().encode('utf-8')
        mainurl = "http://rent.591.com.tw/"
        link = mainurl + href
        log.msg(link, level=log.DEBUG)
        return link
