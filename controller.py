from models import Listing, SearchQuery
from scraper import PreviewScraper, ListingScraper
from serializer import Serializer


class Controller:
	def __init__(self, listings_table, settings_table, config_name, search_query, preview_scraper):
		self.listings_table = listings_table
		self.settings_table = settings_table
		self.config_name = config_name
		self.sq = search_query
		self.ps = preview_scraper

	def fetch_from_airtable(self):
		# config_name = 'basic'
		config_name = self.config_name
		self.sq.fetch_from_airtable(self.settings_table, config_name)

	def get_all_listings_urls(self):				
		# get all the urls
		all_listings = []
		# get all the pages	
		all_pages_urls = self.ps.get_all_pages_urls()
		print("~~~~~~~> fetched all urls:", all_pages_urls)
		# for each page, get the list of listings
		for page_url in all_pages_urls:
			listings_urls = self.ps.get_listings_urls(page_url)
			all_listings += listings_urls
		print("~~~~~~~> fetched all listings urls:", listings_urls)
		return listings_urls

	def create_listings(self, listings_urls):
		print("~~~~~~~> creating listings")
		for url in listings_urls:
			# might be useful to create a "Listing Controller" for that part
			listing_scraper = ListingScraper(url)
			listing = Listing(listings_table = self.listings_table)
			serializer = Serializer(settings_table = self.settings_table)
			lc = ListingController(listing_scraper, listing, serializer)
			df = lc.scrape_listing_df()
			lc.serialize_df_to_dict(df)
			lc.save_listing()



class ListingController:
	def __init__(self, listing_scraper=None, listing=None, serializer=None, dict_data={}):		
		self.ls = listing_scraper
		self.listing = listing
		self.dict_data = dict_data
		self.serializer = serializer

	def scrape_listing_df(self):
		# scrape the data, returns dict		
		url = self.ls.url
		df = self.ls.scrape_listing()
		print("~~~> scraped: ", url)
		return df				

	def serialize_df_to_dict(self, df):		
		dict_data = self.serializer.df_to_dict(df)		
		self.dict_data = dict_data
		return dict_data
		

	def save_listing(self):
		# gets the dict_data and sends it to airtable
		self.listing.save_each_value(self.dict_data)
		