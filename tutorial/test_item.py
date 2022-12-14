import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    tags = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


class DiscoutedProduct(Product):
    discount_persent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()


def my_serializer(value):
    return str(value)


class SpecificProduct(Product):
    name = scrapy.Field(Product.fields['name'], serializer=my_serializer)
