import re
from serializer import Serializer
import json
from pyairtable.formulas import match
from pyairtable import Table
import os


class Settings:

    def __init__(self, api_key, base_name):
        self.api_key = api_key
        self.base_name = base_name
        self.listings_table = Table(api_key, base_name, 'Listings')
        self.settings_table = Table(api_key, base_name, 'Settings')


class SearchQuery:

    # Default settings added here
    def __init__(self, base="https://www.alberlet.hu",
                 language="en",
                 page="1",
                 district="i+v+vi+vii+viii+ix",
                 equipment="2",
                 property_type="apartment",
                 region="budapest",
                 rental_fee_euro="400-900-eur",
                 room="3-x",
                 search="normal",
                 limit="100",
                 min_size="10",
                 keyword="",
                 url=""):

        self.base = base
        self.language = language
        self.page = page
        self.district = district
        self.equipment = equipment
        self.property_type = property_type
        self.region = region
        self.rental_fee_euro = rental_fee_euro
        self.room = room
        self.search = search
        self.limit = limit
        self.min_size = min_size
        self.keyword = keyword
        self.url = url
        self.get_url()

        # https://www.alberlet.hu/en/sublet_to_let/page:201/district:i+v+vi+vii+viii+ix/equipment:2/property-type:apartment/
        # region:budapest/rental-fee-euro:0-900-eur/room:2-x/search:normal/limit:100

    def get_url(self):
        s = self
        self.url = f"{s.base}/{s.language}/sublet_to_let/page:{s.page}/district:{s.district}/equipment:{s.equipment}/keyword:{s.keyword}/property-type:{s.property_type}/size:{s.min_size}-x-m2/region:{s.region}/rental-fee-euro:{s.rental_fee_euro}/room:{s.room}/search:{s.search}/limit:{s.limit}"
        return self.url

    def next_page(self):
        self.page = str(int(self.page) + 1)
        self.get_url()

    def fetch_from_airtable(self, settings_table, config_name):
        serializer = Serializer(settings_table)
        data = serializer.airtable_to_search(config_name)
        self.rental_fee_euro = data['rental_fee_euro']
        self.room = data['room']
        self.min_size = data['min_size']
        self.keyword = data['keyword']


class Listing:
    def __init__(self, listings_table, iterable=(), **kwargs):
        self.listings_table = listings_table
        self.__dict__.update(iterable, **kwargs)

    def save(self, dict_data):
        # s = Serializer()
        # s.df_to_json(dict)
        listing = self.listings_table.first(
            formula=match({"url": dict_data["url"]}))
        if listing:
            self.listings_table.update(listing['id'], dict_data)
        else:
            self.listings_table.create(dict_data)

    def format_nums(self, dict_data):
        # golfing this shit
        try:
            dict_data["Rental price"] = dict_data["New rental price"]
        except:
            pass
        keys = ["Rental price", "Utilities", "Common cost", "Deposit", "Size"]
        dict_data["Total cost"] = 0
        for key in keys:
            if dict_data[key]:
                dict_data[key] = re.findall("\d{1,4}", dict_data[key])[0]
                if key in keys[:3]:
                    dict_data["Total cost"] += int(dict_data[key])
        return dict_data

    def save_each_value(self, dict_data):
        dict_data = self.format_nums(dict_data)
        listing = self.listings_table.first(
            formula=match({"url": dict_data["url"]}))
        if not listing:
            print("Creating a new lising in Airtable")
            listing = self.listings_table.create({"url": dict_data['url']})
            listing['fields']['Status'] = 'New'

        # Do not update listing if the status is 'Not interested'
        if listing['fields']['Status'] != 'Not interested':
            for key in dict_data:
                try:
                    data = {}
                    data[key] = dict_data[key]
                    print(data)
                    self.listings_table.update(listing['id'], data)
                except:
                    print(f"Field {key} couldn't be added!")
                    pass
