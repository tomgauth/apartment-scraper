from scraper import PreviewScraper, ListingScraper
from models import Listing, SearchQuery, Settings
from controller import Controller, ListingController
from serializer import Serializer
from view import MainView


def main():
    view = MainView()
    view.welcome()
    airtable_api = view.set_airtable_api()
    airtable_base = view.set_airtable_base()
    config_name = view.set_config_name()
    settings = Settings(api_key='keyKRBU0MXfsukETM', base_name='app1xRJZRwrHiCDwp')
    listings_table = settings.listings_table
    settings_table = settings.settings_table
    search_query = SearchQuery()   
    preview_scraper = PreviewScraper(search_query)
    controller = Controller(listings_table, settings_table, config_name, search_query, preview_scraper)
    controller.fetch_from_airtable()
    # create search Query    
    all_urls = controller.get_all_listings_urls() 
    controller.create_listings(all_urls)
    



if __name__ == "__main__":
    main()
