import scrapy


class VortaroSpider(scrapy.Spider):
    name = "vortaro"
    allowed_domains = ["io.wiktionary.org"]
    start_urls = ["https://io.wiktionary.org/wiki/Kategorio:Idala_vorti"]

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
        pass
