import scrapy
from DoubanMovie.items import DoubanmovieItem
from scrapy import Request


class DoubanSpider(scrapy.Spider):
    name = "douban"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
    }

    def start_requests(self):
        url = "https://movie.douban.com/top250"
        yield Request(url, headers=self.headers)

    def parse(self, response):
        movies = response.xpath('//ol[@class="grid_view"]/li')

        for movie in movies:
            item = DoubanmovieItem() # 需要在循环里面创建实例，否在会在同一个实例反复写入

            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="bd"]/div/span[2]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="bd"]/div/span[4]/text()'
            ).extract()[0]

            yield item # 输出实例
        
        next_page = response.xpath('//span[@class="next"]/a/@href').get() #翻页
        if next_page:
            next_url = response.urljoin(next_page)
            yield Request(next_url, headers=self.headers, callback=self.parse)
