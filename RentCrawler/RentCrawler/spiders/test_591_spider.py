import scrapy
from scrapy.selector import Selector
import json
from RentCrawler.items import RentItem

class Test591Spider(scrapy.spider.Spider):
    name = "test591"
    allowed_domains = ["rent.591.com.tw"]
    start_urls = [
        "http://rent.591.com.tw/index.php?module=search&action=rslist&is_new_list=1&type=1&searchtype=1&region=3&listview=img&rentprice=3&section=37&pattern=2&order=posttime&orderType=desc"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-1]
        with open('out/' + filename, "wb") as f:
            f.write(response.body.encode('utf-8'))
        data = json.loads(response.body)
        main = data['main']
        #print data['main']
        print "aaaa"


        rents_html = Selector(text=main, type="html").xpath("//div[@class='shList ']")
        #rents_str = rents_html.extract()
        print "len ", len(rents_html)
        #print rents_html[0].extract()

        for rent_html in rents_html:
            item = RentItem()
            item['title'] = self.get_title(rent_html)
            item['price'] = self.get_price(rent_html)
            item['address'] = self.get_address(rent_html)
            item['floor'] = self.get_floor(rent_html)
            item['link'] = self.get_link(rent_html)
            yield item

    def get_title(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        titlediv = datadiv.xpath(".//p[@class='title']//@title")
        title = titlediv[0].extract().encode('utf-8')
        print title
        return title
        #print titlediv.encode('utf-8')

    def get_price(self, rent_html):
        price_str = rent_html \
                    .xpath("//li[@class='price fc-org']//strong[@class='']/text()") \
                    .extract()[0] \
                    .encode("utf-8")
        price_str = ''.join([s for s in price_str if s.isdigit()])
        price = int(price_str)

        print price
        return price

    def get_address(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        addrp = datadiv.xpath("p")[1]
        addr = addrp.xpath("text()")[0].extract().encode("utf-8")
        print addr
        return addr

    def get_floor(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        floorp = datadiv.xpath("p")[2]
        floor = ''.join(floorp.xpath(".//text()").extract()).encode("utf-8")
        print floor
        return floor

    def get_datadiv(self, rent_html):
        datadiv = rent_html.xpath("//div[@class='right']")[0]
        return datadiv

    def get_link(self, rent_html):
        datadiv = self.get_datadiv(rent_html)
        titlep = datadiv.xpath(".//p[@class='title']")
        href = titlep.xpath(".//@href")[0].extract().encode('utf-8')
        mainurl = "http://rent.591.com.tw/"
        link = mainurl + href
        print link
        return link
