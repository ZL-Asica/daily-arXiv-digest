# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import arxiv
import requests


class DailyArxivPipeline:
    """
    Fetches metadata via the arxiv API, writes out items,
    and optionally downloads PDFs into a folder passed via -a pdf=<folder>.
    """

    def open_spider(self, spider):
        self.client = arxiv.Client(page_size=100)
        # capture PDF download target folder
        self.pdf_folder = getattr(spider, "pdf_folder", None)
        if self.pdf_folder:
            os.makedirs(self.pdf_folder, exist_ok=True)

    def process_item(self, item, spider):
        pid = item["id"]
        # construct URLs
        pdf_url = f"https://arxiv.org/pdf/{pid}.pdf"
        abs_url = f"https://arxiv.org/abs/{pid}"
        item.update(
            {
                "pdf": pdf_url,
                "abs": abs_url,
            }
        )
        # fetch metadata via arxiv API
        search = arxiv.Search(id_list=[pid])
        paper = next(self.client.results(search))
        item.update(
            {
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "categories": paper.categories,
                "comment": paper.comment,
                "summary": paper.summary,
            }
        )
        # optionally download PDF
        if self.pdf_folder:
            resp = requests.get(pdf_url)
            path = os.path.join(self.pdf_folder, f"{pid}.pdf")
            with open(path, "wb") as f:
                f.write(resp.content)
        return item
