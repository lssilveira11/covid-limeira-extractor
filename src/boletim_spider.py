# https://docs.scrapy.org/en/latest/intro/tutorial.html

import scrapy
from datetime import datetime

class BoletimSpider(scrapy.Spider):
    name = "boletim"
    base_url = 'https://www.limeira.sp.gov.br/sitenovo/'

    def start_requests(self):
        articles = []
        start_id = 11543
        end_id = 11800

        for i in range(start_id, end_id):
          articles.append({
            'id': i,
            'url': 'https://www.limeira.sp.gov.br/sitenovo/news_hotsite.php?id=69&news=' + str(i)
          })

        for article in articles:
            yield scrapy.Request(url=article['url'],
              callback=self.parse, 
              meta={'id': article['id']})
            

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
        
        dt_str = response.css('#date_page_content_simple ::text').get()
        dt = datetime.strptime(dt_str, '%d/%m/%Y | %Hh%M')

        yield { 
          'id': response.meta['id'],
          'date' : dt,
          'img_url' : self.base_url + response.css("#print2 > div > img ::attr(src)").get()
        } 