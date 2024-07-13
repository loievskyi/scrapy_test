from typing import Any

import scrapy
from scrapy.http import Response


class KelmImmobilienSpider(scrapy.Spider):
    name = "kelm_immobilien"
    allowed_domains = ["kelm-immobilien.de"]
    start_urls = ["https://kelm-immobilien.de/immobilien/"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        details_urls = response.css(
            "div.property-container "
            "a.btn.btn-default.btn-sm[role='button']"
            ":not([href=''])"
            "::attr(href)").getall()
        for url in details_urls:
            yield scrapy.Request(url, callback=self.parse_details)

        next_page = response.css("link[rel='next']::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_details(self, response: Response, **kwargs: Any) -> Any:
        pass
