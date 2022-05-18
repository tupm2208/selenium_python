import scrapy

class Address(scrapy.Spider):
    name = 'japaneseAddress'
    start_urls = [
        "https://japan-postcode.810popo.net/aichiken/",
        "https://japan-postcode.810popo.net/akitaken/",
        "https://japan-postcode.810popo.net/aomoriken/",
        "https://japan-postcode.810popo.net/chibaken/",
        "https://japan-postcode.810popo.net/ehimeken/",
        "https://japan-postcode.810popo.net/fukuiken/",
        "https://japan-postcode.810popo.net/fukuokaken/",
        "https://japan-postcode.810popo.net/fukushimaken/",
        "https://japan-postcode.810popo.net/gifuken/",
        "https://japan-postcode.810popo.net/gummaken/",
        "https://japan-postcode.810popo.net/hiroshimaken/",
        "https://japan-postcode.810popo.net/hokkaido/",
        "https://japan-postcode.810popo.net/hyogoken/",
        "https://japan-postcode.810popo.net/ibarakiken/",
        "https://japan-postcode.810popo.net/ishikawaken/",
        "https://japan-postcode.810popo.net/iwateken/",
        "https://japan-postcode.810popo.net/kagawaken/",
        "https://japan-postcode.810popo.net/kagoshimaken/",
        "https://japan-postcode.810popo.net/kanagawaken/",
        "https://japan-postcode.810popo.net/kochiken/",
        "https://japan-postcode.810popo.net/kumamotoken/",
        "https://japan-postcode.810popo.net/kyotofu/",
        "https://japan-postcode.810popo.net/mieken/",
        "https://japan-postcode.810popo.net/miyagiken/",
        "https://japan-postcode.810popo.net/miyazakiken/",
        "https://japan-postcode.810popo.net/naganoken/",
        "https://japan-postcode.810popo.net/nagasakiken/",
        "https://japan-postcode.810popo.net/naraken/",
        "https://japan-postcode.810popo.net/nigataken/",
        "https://japan-postcode.810popo.net/oitaken/",
        "https://japan-postcode.810popo.net/okayamaken/",
        "https://japan-postcode.810popo.net/okinawaken/",
        "https://japan-postcode.810popo.net/osakafu/",
        "https://japan-postcode.810popo.net/sagaken/",
        "https://japan-postcode.810popo.net/saitamaken/",
        "https://japan-postcode.810popo.net/shigaken/",
        "https://japan-postcode.810popo.net/shimaneken/",
        "https://japan-postcode.810popo.net/shizuokaken/",
        "https://japan-postcode.810popo.net/tochigiken/",
        "https://japan-postcode.810popo.net/tokushimaken/",
        "https://japan-postcode.810popo.net/tokyoto/",
        "https://japan-postcode.810popo.net/tottoriken/",
        "https://japan-postcode.810popo.net/toyamaken/",
        "https://japan-postcode.810popo.net/wakayamaken/",
        "https://japan-postcode.810popo.net/yamagataken/",
        "https://japan-postcode.810popo.net/yamaguchiken/",
        "https://japan-postcode.810popo.net/yamanashiken/"
    ]

    def parse(self, response):
        url = response.request.url.strip("/")
        prop = url.split("/")[-1]
        for link in response.css('.links ul li a'):
            next_link = response.request.url + link.xpath('@href').extract()[0]
            yield response.follow(next_link, self.parse_main_page)

    def parse_main_page(self, response):
        url = response.request.url.strip("/")
        data = []
        for link in response.css('.links ul li a'):
            d = link.xpath('@href').extract()[0].replace(".html", "")
            name = link.xpath('span/text()').extract_first()
            yield {"link": f'{url.replace(".html", "")}/{d}/{name}'}
            break