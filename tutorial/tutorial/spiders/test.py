from urllib.parse import urlencode
import scrapy

API_KEY = '7d519771f54a35e6362f66c7b4ee8152'


def proxy(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class QuotesSpider(scrapy.Spider):
    name = "test"
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def start_requests(self):
        yield scrapy.Request(url=proxy(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.product-item-info'):
            yield {
                'name': quote.css('a.product-item-link::text').get(),
                'price': quote.css('span.price::text').get().replace('£', ''),
                'link': quote.css('a.product-item-link').attrib['href']
            }
        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
