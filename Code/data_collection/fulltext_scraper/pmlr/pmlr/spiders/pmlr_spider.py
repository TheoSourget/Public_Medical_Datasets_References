# import urlparse
import scrapy

from scrapy.http import Request
import urllib
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from pydispatch import dispatcher
"""
Exemple of usage
scrapy crawl pmlr -a start_url=143,121
143 and 121 being the volume number of the venue
"""

class PMLRSpider(scrapy.Spider):
    name = "pmlr"

    def __init__(self, start_url, **kwargs):

        """
        Instantiate the spider.
        @param kwargs: keyword arguments
        """
        # the base url common to all urls; just a convenience variable so that we do not have to repeat it
        self.base_url = 'https://proceedings.mlr.press/v'

        # flag to signal if the crawl is in persistent mode
        self.is_persistent = False
        self.start_url = start_url.split(',')
        super().__init__(**kwargs)

    def start_requests(self):
        urls = self.start_url
        for volume_id in urls:
            yield scrapy.Request(url=f"https://proceedings.mlr.press/v{volume_id}", callback=self.parse)

    def parse(self, response):

        for article in response.xpath('/html/body/main/div/div[*]'):
            try:
                yield Request(
                    url=article.xpath('p[3]/a[2]/@href').get(),
                    meta={
                        "title": article.xpath('p[1]/text()').get()
                        },
                    callback=self.save_pdf
                )
            except Exception as e:
                print(e)

    def save_pdf(self, response):
        try:
            # path = response.url.split('/')[-1]
            if "Preface" not in response.meta['title']:
                title = response.meta['title'].replace("/"," ").removesuffix(".")+".pdf"
                self.logger.info('Saving PDF %s', title)
                with open(f"../../../../Results/extraction/fulltext/{title}", 'wb') as f:
                    f.write(response.body)
        except Exception as e:
            print(e)