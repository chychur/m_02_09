import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from mongoengine import connect

from models import Authors, Quotes


# Connection to the  MongoDB
connect(
    db='web139hw',  # DB name
    host='mongodb+srv://chychur:VuMoT5JYjeOMrgyk@clusterb.sffzgqf.mongodb.net/?retryWrites=true&w=majority',
    alias='default',
    ssl=True
)


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    full_name = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "full_name" in adapter.keys():
            self.authors.append(
                {
                    "full_name": adapter["full_name"],
                    "born_date": adapter["born_date"],
                    "born_location": adapter["born_location"],
                    "description": adapter["description"],
                })

        if "quote" in adapter.keys():
            self.quotes.append(
                {
                    "tags": adapter["tags"],
                    "author": adapter["author"],
                    "quote": adapter["quote"],
                })
        return item

    def close_spider(self, spider):
        with open("quotes.json", "w", encoding="utf-8") as file:
            json.dump(self.quotes, file, ensure_ascii=False, indent=4)
        with open("authors.json", "w", encoding="utf-8") as file:
            json.dump(self.authors, file, ensure_ascii=False, indent=4)

        with open("authors.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                author = Authors(
                    full_name=item.get("full_name"),
                    born_date=item.get("born_date"),
                    born_location=item.get("born_location"),
                    description=item.get("description")
                ).save()

        with open("quotes.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                author_name = item.get("author")
                author = Authors.objects(full_name=author_name).first()
                quote = Quotes(
                    tags=item.get("tags"),
                    author=author,
                    quote=item.get("quote")
                ).save()


# Scrapy web spider definition
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com']
    custom_settings = {'ITEM_PIPELINES': {QuotesPipeline: 100}}

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get()
            q = quote.xpath("span[@class='text']/text()").get()
            yield QuoteItem(tags=tags, author=author, quote=q)
            yield response.follow(
                url=self.start_urls[0] + quote.xpath("span//a/@href").get(),
                callback=self.parse_about_author,
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_about_author(self, response):
        about = response.xpath("/html//div[@class='author-details']")
        full_name = about.xpath("h3[@class='author-title']/text()").get()
        born_date = about.xpath("p/span[@class='author-born-date']/text()").get()
        born_location = about.xpath(
            "p/span[@class='author-born-location']/text()"
        ).get()
        description = (
            about.xpath("div[@class='author-description']/text()").get().strip()
        )
        yield AuthorItem(
            full_name=full_name,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
