import os

import scrapy


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    allowed_domains = ["arxiv.org"]

    def __init__(self, pdf=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Read categories from environment
        env = os.environ.get("CATEGORIES", "cs.HC,cs.LG,cs.CL")
        cats = [c.strip() for c in env.split(",") if c.strip()]
        self.start_urls = [f"https://arxiv.org/list/{c}/new" for c in cats]
        # Optional folder to download PDFs into
        self.pdf_folder = pdf

    def parse(self, response):
        # extract new-paper identifiers
        ids = []
        for li in response.css("div#dlpage ul li"):
            # e.g. '/abs/XXXX'
            href = li.css("a::attr(href)").get()
            if href and "/abs/" in href:
                ids.append(href.split("/")[-1])

        # parse each entry on the page
        for dt in response.css("dl dt"):
            pid = dt.css("a[title='Abstract']::attr(href)").get().split("/")[-1]
            # skip entries newer than the first li
            if ids and pid >= ids[-1]:
                continue
            yield {"id": pid}
