import scrapy
from ..items import TutorialItem
from scrapy.loader import ItemLoader
from urllib.parse import urlencode

API_KEY = '7d519771f54a35e6362f66c7b4ee8152'


def proxy(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class WhiskySpider(scrapy.Spider):
    name = 'whisky'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def start_requests(self):
        yield scrapy.Request(url=proxy(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            loader = ItemLoader(item=TutorialItem(), selector=products)

            loader.add_css('name', 'a.product-item-link')
            loader.add_css('price', 'span.price')
            loader.add_css('link', 'a.product-item-link::attr(href)')

            yield loader.load_item()

        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
