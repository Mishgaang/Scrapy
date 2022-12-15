import time

import scrapy
from scrapy_playwright.page import PageMethod


class WildberriesSpider(scrapy.Spider):
    name = 'wildberries'

    def start_requests(self):
        url = 'https://www.wildberries.ru/catalog/knigi/detyam-i-roditelyam/noviy-god-i-rozhdestvo?bid=84d80778-9e50-427e-a57d-134ed224493f'
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.product-card__wrapper')
            ],
            errback=self.errback
        ))

    def parse(self, response):
        book_page_link = response.css('div.product-card__wrapper::attr(href)')
        yield from response.follow_all(book_page_link, self.book_parse)
        pagination_link = response.css('a.pagination__next::attr(href)')
        yield from response.follow_all(pagination_link, self.parse)

    def book_parse(self, response):
        def extract_with_css(query):
            return response.css(query).get()

        yield {
            'title': extract_with_css('div.product-page__header h1::text'),
            'price': extract_with_css('ins.price-block__final-price::text')
        }

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
