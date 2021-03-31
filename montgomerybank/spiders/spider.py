import scrapy

from scrapy.loader import ItemLoader

from ..items import MontgomerybankItem
from itemloaders.processors import TakeFirst
import requests


class MontgomerybankSpider(scrapy.Spider):
	name = 'montgomerybank'
	start_urls = ['https://www.montgomerybank.com/blog/']

	def parse(self, response):
		data = requests.request("GET", "https://www.montgomerybank.com/blog/", headers={}, data={})
		raw_data = scrapy.Selector(text=data.text)

		post_links = raw_data.xpath('//p[contains(@class,"link-more")]/a/@href').getall()
		for url in post_links:
			yield response.follow(url, self.parse_post, cb_kwargs={'url': url}, dont_filter=True)

	def parse_post(self, response, url):
		data = requests.request("GET", url, headers={}, data={})
		raw_data = scrapy.Selector(text=data.text)
		title = raw_data.xpath('//h1/text()').get()
		description = raw_data.xpath('//div[@class="site-content-contain"]//div[@class="wpb_wrapper"]//div[@class="wpb_wrapper"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=MontgomerybankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
