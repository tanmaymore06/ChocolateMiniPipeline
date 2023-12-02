# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PriceToRupeePipeline:
    """ This class converts price from British Pounds to Indian rupees"""

    Conversion_factor = 104.58


    def process_item(self, item, spider):
        adapter = ItemAdapter(item) # Storing all the values of all the fields into the adapter local-variable
                                    # If you want to get values of a field then, adapter['field_name'] like a dictionary   
        if adapter.get('price_inrupees'):
            float_price = float(adapter['price_inrupees'])
            adapter['price_inrupees'] = float_price * self.Conversion_factor # self.Conversion_factor for accessing the Conversion_factor global-variable
            return item 
        else:
            raise DropItem("Missing price {item}")
        


class DuplicatesPipeline:
    def __init__(self):
        self.names_seen = set() # A class variable having an empty set, and we'll store names which are present in the 'name' field
        
        def process_item(self, item, spider):
            adapter = ItemAdapter(item)

            if adapter['name'] in self.names_seen:
                raise DropItem("Duplicate item found: {item!r}")
            else:
                self.names_seen.add(adapter['name'])
                return item 

import mysql.connector

class SavingToMysqlPipeline(object):
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'dolsurphin01',
            database = 'chocolate_scraping'
        )
        self.curr = self.connection.cursor()
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    def store_db(self, item):
        self.curr.execute(""" insert into chocolate_products (name, price_inrupees, url) values (%s, %s, %s)""", (
            item["name"],
            item["price_inrupees"],
            item["url"]
        ))
        self.connection.commit()