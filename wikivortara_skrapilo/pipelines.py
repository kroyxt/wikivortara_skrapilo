# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class WikivortaraSkrapiloPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        datuma_nomi = adapter.field_names()
        for datuma_nomo in datuma_nomi:
            datuma_valoro = adapter.get(datuma_nomo)

            if datuma_nomo == "traduki":
                for traduko in datuma_valoro:
                    valoro = re.sub(r"<([a-z]+)(?![^>]*\/>)[^>]*>", "", datuma_valoro[traduko])
                    valoro = re.sub(r"</([a-z]+)>", "", valoro)
                    valoro = valoro.replace("[[", "")
                    if f"{traduko.capitalize()}:" in valoro:
                        valoro = valoro.replace(f"{traduko.capitalize()}:", "")
                    adapter[datuma_nomo][traduko] = valoro.lower().strip()
            else:
                valoro = re.sub(r"<([a-z]+)(?![^>]*\/>)[^>]*>", "", datuma_valoro)
                valoro = re.sub(r"</([a-z]+)>", "", valoro)
                if f"{datuma_nomo.capitalize()}:" in valoro:
                    valoro = valoro.replace(f"{datuma_nomo.capitalize()}:", "")
                adapter[datuma_nomo] = valoro.lower().strip()

        return item
