import pprint
import re
from typing import Any, List

import scrapy
from scrapy.http import Response

from udata_test.items import RentalItem


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
        item = RentalItem(
            url=response.url,
            title=self._get_title(response),
            status=self._get_status(response),
            pictures=self._get_pictures(response),
            rent_price=self._get_rent_price(response),
            description=self._get_description(response),
            phone_number=self._get_phone_number(response),
            email=self._get_email(response),
        )
        pprint.pprint(item)
        return item

    def _get_title(self, response: Response) -> str | None:
        return response.css("h1.property-title::text").get()

    def _get_status(self, details_response: Response) -> str | None:
        return (details_response
                .css("li.list-group-item.data-vermietet .dd::text")
                .get())

    def _get_pictures(self, details_response: Response) -> List[str]:
        return (details_response
                .css("div#immomakler-galleria a img::attr(data-big)")
                .getall())

    def _convert_price(self, price: str) -> float | None:
        try:
            price = price.replace(".", "")
            price = re.sub(r"[^\d.,]", "", price)
            return float(price)
        except Exception:
            return None

    def _get_purchase_price(self, details_response: Response) -> str | None:
        price = (details_response
                 .css("li.list-group-item.data-kaufpreis .dd::text")
                 .get())
        if price is not None:
            return self._convert_price(price)
        return None

    def _get_rent_price(self, details_response: Response) -> str | None:
        price = (details_response
                 .css("li.list-group-item.data-kaltmiete .dd::text")
                 .get())
        if price is not None:
            return self._convert_price(price)
        return None

    def _get_description(self, details_response: Response) -> str | None:
        description = details_response.css(
            "div.property-description .panel-body h3, "
            "div.property-description .panel-body p")
        description_text = ""
        tag_header = ""
        tag_text = ""
        for description_part in description:
            if description_part.root.tag == "h3":
                if tag_text:
                    description_text += f"{tag_header}\n{tag_text.strip()}\n"
                tag_header = description_part.css("::text").get()
                tag_text = ""
            elif description_part.root.tag == "p":
                tag_text += f"{description_part.css('::text').get().strip()} "
        description_text += f"{tag_header}\n{tag_text.strip()}"
        return description_text

    def _get_phone_number(self, details_response: Response) -> str | None:
        return (details_response
                .css(".property-contact .dd.col-sm-7.p-tel.value a::text")
                .get())

    def _get_email(self, details_response: Response) -> str | None:
        return (details_response
                .css(".property-contact .dd.col-sm-7.u-email.value a::text")
                .get())
