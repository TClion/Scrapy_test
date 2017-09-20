import scrapy
from douban_book.items import DoubanBookItem


class douban_book(scrapy.Spider):
    name = "douban_book"
    allowed_domains = ['douban.com']
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'book.douban.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://book.douban.com/tag/'
        yield scrapy.Request(url, headers=self.header, callback=self.parse_item_url)

    def parse_item_url(self, response):
        for item_url in response.xpath('//table[@class="tagCol"]//td/a/@href').extract():
            # item_url = response.urljoin(item_url)
            yield response.follow(item_url, headers=self.header, callback=self.parse_info_url)

    def parse_info_url(self, response):
        for info_url in response.xpath('//div[@class="info"]/h2/a/@href').extract():
            yield scrapy.Request(info_url, headers=self.header, callback=self.parse)
        next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, headers=self.header, callback=self.parse_info_url)

    def parse(self, response):
        title = response.xpath('//h1/span[1]/text()').extract_first()
        link = response.url
        author = response.xpath('//div[@id="info"]//a[1]/text()').extract_first().replace('\n','').replace('\r','').replace('\t','').strip()
        score = response.xpath('//strong[@class="ll rating_num "]/text()').extract_first()
        # print title
        # print link
        # print author
        # print score
        item = DoubanBookItem()
        item['title'] = title
        item['link'] = link
        item['author'] = author
        item['score'] = score
        yield item



