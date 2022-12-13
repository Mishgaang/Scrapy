import scrapy


class Games_catalog(scrapy.Spider):
    name = 'games'

    start_urls = ['https://stopgame.ru/games/catalog']

    def parse(self, response):
        game_page_link = response.css('._card_67304_1')
        yield from response.follow_all(game_page_link, self.parse_game)

        paginayiom_links = response.css('a.next')
        yield from response.follow_all(paginayiom_links, self.parse)

    def parse_game(self, response):
        def extract_with_css(query):
            return response.css(query).get()

        yield {
            'title': extract_with_css('h1._title_5jdno_273::text'),
            'dev': extract_with_css('div._info-grid__value_yxhdd_198:nth-child(4) a::text'),
            'date': extract_with_css('div._info-grid__value_yxhdd_198:nth-child(12)::text')
        }


class Esports_news(scrapy.Spider):
    name = 'news'

    start_urls = ['https://stopgame.ru/news/cybersport']

    def parse(self, response):
        news_page_link = response.css('div.caption-bold a::attr(href)')
        yield from response.follow_all(news_page_link, self.parse_news)

        pagination_link = response.css('a.next::attr(href)')
        yield from response.follow_all(pagination_link, self.parse)

    def parse_news(self, response):
        def extract_with_css(query):
            return response.css(query).get()

        yield {
            'title': extract_with_css('div._material-info_1622n_134 h1::text'),
            'author': extract_with_css('div._bottom-info_1622n_573 span::text'),
            'link': extract_with_css('head meta:nth-child(8)::attr(content)'),
            'date': extract_with_css('span._date_1622n_526::text'),
            'number_of_views': extract_with_css('div._top-info_1622n_479 span:nth-child(4)::text')
        }
