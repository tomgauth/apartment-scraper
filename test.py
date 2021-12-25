from models import Listing, SearchQuery
from scraper import PreviewScraper, ListingScraper
from controller import Controller

apt_url = "https://www.alberlet.hu/en/sublet_to_let/budapest-7-district-nefelejcs-utca-43m2-2-room_672955"

url2 = "https://www.alberlet.hu/en/sublet_to_let/budapest-8-district-rakoczi-ut-31m2-2-room_860237"

def run_test():    
    ls = ListingScraper(url = url2)
    dict_data = ls.scrape_listing()
    print(dict_data)
    listing = Listing()
    listing.save_each_value(dict_data)


controller = Controller()
# create search Query
sq = SearchQuery()
# get all the pages
ps = PreviewScraper(search_query = sq)
ls = ListingScraper(url=sq.url())
listing = Listing()
all_pages = ps.get_all_pages_urls()
for page in all_pages:
    print("scraping page", page)
    ps.url = page
    listings_urls = ps.get_listings_urls()
    for listing_url in listings_urls:
        ls.url = listing_url
        dict_data = ls.scrape_listing()        
        listing.save_each_value(dict_data)
