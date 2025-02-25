import scrapy

from ..items import BookDetailItem

class BookSpider(scrapy.Spider):
    name = "Books"
    start_urls = ["https://books.toscrape.com/index.html"]

    def parse(self, response):
        for books in response.css('article.product_pod'):
            title = books.css('h3 a::attr(title)').get()
            price = books.css('p.price_color::text').get().replace('£', '') 
            book_url = books.css('h3 a::attr(href)').get()
            full_book_url = response.urljoin(book_url)

            
            yield response.follow(full_book_url, callback=self.parse_book, meta={'title': title, 'price': price, 'book_url': full_book_url})

  
        # next_page_url = response.css('li.next a::attr(href)').get()
        # if next_page_url:
        #     full_next_page_url = response.urljoin(next_page_url)
        #     yield response.follow(full_next_page_url, callback=self.parse)

    def parse_book(self, response):
        
        title = response.meta['title']
        price = response.meta['price']
        book_url = response.meta['book_url']

     
        categories = response.css('ul.breadcrumb li a::text').getall()
        category = categories[-1] if categories else "Unknown"

   
        upc = response.css('table tr:nth-child(1) td::text').get()
        product_type = response.css('table tr:nth-child(2) td::text').get()
        price_excl_tax = response.css('table tr:nth-child(3) td::text').get()
        price_incl_tax = response.css('table tr:nth-child(4) td::text').get()
        tax = response.css('table tr:nth-child(5) td::text').get()
        availability = response.css('table tr:nth-child(6) td::text').get()
        num_reviews = response.css('table tr:nth-child(7) td::text').get()
      
        book_details = BookDetailItem(
            category = category,
            availability = availability,
            title = title,
            price = price

        )


        # yield {
        #     'book_title': title,
        #     'book_price': price,
        #     'book_url': book_url,
        #     'category': category,
        #     'UPC': upc,
        #     'product_type': product_type,
        #     'price_excl_tax': price_excl_tax,
        #     'price_incl_tax': price_incl_tax,
        #     'tax': tax,
        #     'availability': availability,
        #     'num_reviews': num_reviews
        # }
        yield book_details