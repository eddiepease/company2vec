from scrapy import Item, Field


class WebsiteItem(Item):

    """
    Defines the item output
    """

    company_url = Field()
    company_text = Field()