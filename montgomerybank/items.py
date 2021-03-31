import scrapy


class MontgomerybankItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
