
import scrapy

class google(scrapy.Spider):
    name = "google"
    allowed_domains = ["example.com"]

    def parse(self, response):
        for h3 in response.xpath("//h3").getall():
            yield {"title": h3}

        for href in response.xpath("//a/@href").getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
        