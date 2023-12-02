from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


class ChocolateProductLoader(ItemLoader):
    """ This class provides a machenism to load data into item"""


    default_output_processor = TakeFirst()
    price_inrupees_in = MapCompose(lambda x: x.split("£")[-1])
    url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x)