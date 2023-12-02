import scrapy
from scrapy_prac1.items import ChocolateProduct    # scrapy.items helps to organize our scraped items 
from scrapy_prac1.itemloaders import ChocolateProductLoader # itemloaders take items given by our spider then, processes it, and stores it in item

class ChocolateSpiderSpider(scrapy.Spider):
    """ 
    This will present the main code for logic of scraping data,
    how to process it, and 
    how to store it in a relavent data repository
    """

    name = "chocolate_spider" # name of our spider
    allowed_domains = ["chocolate.co.uk"] # The main website for scraping data
    start_urls = ["https://www.chocolate.co.uk/collections/all"] #The location of the page from where, we want to scrape data

    def parse(self, response):
        """
        This is the function which, if you give a starting_url then, 
        with the logic of getting the data, it will parse it
        """
        
        products = response.css('product-item') # All the products of a single page
        
        
        for product in products:

            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector= product)  #Instantiating the 'chocolate' object of the ChocolateProductLoader class imported from the ItemLoaders
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            chocolate.add_css('price_inrupees' , 'span.price', re ='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>'),
            chocolate.add_css('url' , 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item() # loads values into the ChocolateProduct() i.e., in item

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page #This is the full link to the next page
            yield response.follow(next_page_url, callback = self.parse) #The response.follow() dictates our spider to follow the given link and extracts data with the parse method
