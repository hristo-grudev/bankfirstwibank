import scrapy

from scrapy.loader import ItemLoader

from ..items import BankfirstwibankItem
from itemloaders.processors import TakeFirst


class BankfirstwibankSpider(scrapy.Spider):
	name = 'bankfirstwibank'
	start_urls = ['https://bankfirstwi.bank/news.html']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//main//text()[normalize-space() and not(ancestor::h1 | ancestor::time | ancestor::span)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=BankfirstwibankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
