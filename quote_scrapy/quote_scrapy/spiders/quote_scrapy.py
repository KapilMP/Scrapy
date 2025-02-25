import scrapy

class QuoteSpider(scrapy.Spider):
    name = "Quote"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        for quotes in response.css('div.quote'):
            author_url = quotes.css('span a::attr(href)').get()
            full_author_url = response.urljoin(author_url) if author_url else None

            yield {
                'quote': quotes.css('span.text::text').get().replace("“", ""),
                'author': quotes.css('small.author::text').get(),
                'author-url': full_author_url
            }

        
        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url:
            full_next_page_url = response.urljoin(next_page_url)
            yield response.follow(full_next_page_url, callback=self.parse)
