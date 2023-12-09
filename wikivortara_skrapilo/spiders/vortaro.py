import scrapy
from wikivortara_skrapilo.items import WikivortaraSkrapiloItem


class VortaroSpider(scrapy.Spider):
    name = "vortaro"
    allowed_domains = ["io.wiktionary.org"]
    start_urls = ["https://io.wiktionary.org/wiki/Kategorio:Idala_vorti"]
    custom_settings = {
        'FEEDS': {
            'vortaro.json': {'format': 'json', 'overwrite': True},
        }
    }

    def parse(self, response):
        # Kolektez omna ligili di vorta secioni
        vortara_ligili = response.xpath(
            "//div[@class='mw-category-group']/ul/li/div/div/a/@href"
        )
        # Irez ad omna vortara ligili
        for vortara_ligilo in vortara_ligili:
            vortara_seciono = f"https://io.wiktionary.org/{vortara_ligilo.get()}"
            yield response.follow(
                vortara_seciono,
                callback=self.parse_vortara_seciono
            )

        # Serchez la ligilo por irar ad la sequanta pagino
        sequante_pagina_ligili = response.xpath(
            "//div[@id='mw-subcategories']/a[contains(text(), 'sequanta')]/@href"
        )
        # Se ligilo ad sequanta pagino existas, irez ad sequanta pagino
        if len(sequante_pagina_ligili) > 1:
            sequanta_pagino = f"https://io.wiktionary.org/{sequante_pagina_ligili[0].get()}"
            yield response.follow(
                sequanta_pagino,
                callback=self.parse,
            )

    def parse_vortara_seciono(self, response):
        # Kolektez omnia ligili di vorti
        vorta_ligili = response.xpath(
            "//div[@class='mw-category-group']/ul/li/a/@href"
        )
        # Irez ad omna vorta ligili
        for vorta_ligilo in vorta_ligili:
            relativa_ligilo = f"https://io.wiktionary.org/{vorta_ligilo.get()}"
            yield response.follow(
                relativa_ligilo,
                callback=self.parse_vorto
            )

        # Serchez la ligilo por irar ad la sequanta pagino
        sequante_pagina_ligili = response.xpath(
            '//div[@id="mw-pages"]/a[contains(text(), "sequanta")]/@href'
        )
        # Se ligilo ad sequanta pagino existas, irez ad sequanta pagino
        if len(sequante_pagina_ligili) > 1:
            sequanta_pagino = f"https://io.wiktionary.org{sequante_pagina_ligili[0].get()}"
            yield response.follow(
                sequanta_pagino,
                callback=self.parse_vortara_seciono
            )

    def parse_vorto(self, response):
        # Kreez variablo datumo di tipo Item por futura netigado
        datumo = WikivortaraSkrapiloItem()
        # Insertez omna datumo en la variablo datumo
        datumo["nomo"] = response.xpath(
            '//h1[@id="firstHeading"]/span/text()'
        ).get()

        vorta_datumi = response.xpath(
            "//div[@class='mw-content-ltr mw-parser-output']/table[@border='1']/tbody/tr/td/ul/li"
        )
        for vorta_datumo in vorta_datumi:
            if "Semantiko" in vorta_datumo.get():
                datumo["semantiko"] = vorta_datumo.get()
            elif "Morfologio" in vorta_datumo.get():
                datumo["morfologio"] = vorta_datumo.get()
            elif "Exemplaro" in vorta_datumo.get():
                datumo["exemplaro"] = vorta_datumo.get()
            elif "Sinonimo" in vorta_datumo.get():
                datumo["sinonimo"] = vorta_datumo.get()
            elif "Antonimo" in vorta_datumo.get():
                datumo["antonimo"] = vorta_datumo.get()

        traduki = response.xpath(
            "//div[@class='mw-content-ltr mw-parser-output']/table[@border='1']/tbody/tr/td[@bgcolor='#f9f9f9']/table/tbody/tr/td/ul/li"
        )
        for traduko in traduki:
            if "Angliana" in traduko.get():
                datumo["angliana"] = traduko.get()
            elif "Franciana" in traduko.get():
                datumo["franciana"] = traduko.get()
            elif "Germaniana" in traduko.get():
                datumo["germaniana"] = traduko.get()
            elif "Hispaniana" in traduko.get():
                datumo["hispaniana"] = traduko.get()
            elif "Italiana" in traduko.get():
                datumo["italiana"] = traduko.get()
            elif "Rusiana" in traduko.get():
                datumo["rusiana"] = traduko.get()

        # Kreez la strukturo finala de la kolektita datumi
        vorto = {
            "nomo": datumo["nomo"],
            "semantiko": datumo["semantiko"],
            "morfologio": datumo["morfologio"],
            "exemplaro": datumo["exemplaro"],
            "sinonimo": datumo["sinonimo"],
            "antonimo": datumo["antonimo"],
            "traduki": {
                "angliana": datumo["angliana"],
                "franciana": datumo["franciana"],
                "germaniana": datumo["germaniana"],
                "hispaniana": datumo["hispaniana"],
                "italiana": datumo["italiana"],
                "rusiana": datumo["rusiana"]
            }
        }

        yield vorto
