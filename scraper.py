from bs4 import BeautifulSoup
import requests
from models import Listing
import pandas as pd
from serializer import Serializer
import re
import os




class PreviewScraper:

    def __init__(self, search_query, url="", soup=None):        
        self.search_query = search_query
        self.url = url
        self.soup = soup
        self.get_url()
        self.generate_soup()

    def get_url(self):
        self.url = self.search_query.url
        return self.url

    def generate_soup(self):
        self.get_url()
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.soup = soup

    def get_listings_urls(self, first_page_url):
        urls = []
        r = requests.get(first_page_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        main = soup.find("div", {"id": "listing-index"})
        listings_thumbnails = main.find_all("div", {"class": "advert"})
        for l in listings_thumbnails:
            ad_img_link = l.find("a", {"class": "advert__image-link"})
            urls.append(ad_img_link["href"])

        return urls

    def check_last_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        pagination = soup.find("ul", {"class": "pagination"})
        if pagination.find("li", {"class": ["last", "paging-next"]}):
            return False
        else:
            return True

    def get_all_pages_urls(self):
        pages_urls = []

        # LIMITED for testing
        while len(pages_urls) < 50:
            url = self.search_query.url
            pages_urls.append(url)
            print("~~> added page: ", self.search_query.page)
            self.search_query.next_page()

            try:
                if self.check_last_page(url):
                    break
            except:
                continue

        return pages_urls


class ListingScraper:

    def __init__(self, url, soup=None):
        self.url = url
        self.soup = soup
        self.generate_soup()

    def generate_soup(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.soup = soup

    def scrape_tables(self):
        rows = []
        tables = self.soup.find_all("table", class_=["profile-table", "profile__text-data"])         
        try:
            for table in tables:
                for sibling in table.tr.next_siblings:
                    row = []
                    print(sibling)
                    for td in sibling:
                        print("td: ", td)                                               
                        try:
                            if td != ' ': 
                                row.append(td.text.replace('\n', ''))                                                        
                        except:
                            # print("error adding value to row")
                            continue
                    print(row)
                    if len(row) > 0:
                        print(len(row))
                        rows.append(row)
        except:
            print("Error adding rows to the table")
            pass 
        return rows

    def scrape_details(self):
      find = self.soup.find
      rows = []
      apt_features = find("p", class_="profile-info-panels__text")        
      if apt_features:
          rows.append([apt_features.b.text.replace('\n', ''),
                       apt_features.b.next_sibling.text.replace('\n', '')])

      try:
          description = find("div", class_="profile__text")
          rows.append(["description", description.text.replace('\n', '')])
      except:
          print("couldn't add the description")

      try:
          title = find("div", class_="profile__header-container")   
          rows.append(["title", title.text.replace('\n', '')])
      except:
          print("couldn't add the title")

      images_urls = self.scrape_img_urls()
      if images_urls:
          rows.append(["images", images_urls])

      return rows


    def scrape_listing(self):
        # returns a dict with all the values to save        
        table = []
        table_rows = self.scrape_tables()
        details_rows = self.scrape_details()
        url_row = [["url", self.url]]
        table += table_rows + details_rows + url_row
            
        df = pd.DataFrame(table)        
        df.dropna() 
        print(df)               
        return df

    # def scrape_map(self):
    #     # not completed - experimental feature
    #     url = self.url
    #     driver = webdriver.Chrome()
    #     driver.get(url) 
    #     time.sleep(5)
    #     driver.set_window_size(100,1000)
    #     # accept cookies        
    #     driver.find_element_by_css_selector('.cc_btn.cc_btn_accept_all').click()
    #     driver.find_element_by_class_name("ol-zoom-out").click()
    #     report_button = driver.find_element_by_class_name("report")
    #     map_ = driver.find_element_by_class_name('ol-unselectable')
    #     actions = ActionChains(driver)
    #     actions.move_to_element(report_button).perform()
    #     time.sleep(4)
    #     # save map_
    #     # Upload to dropbox
    #     file_name = re.findall('\d{6}', url)[0]
    #     map_.screenshot(f'{file_name}.png')
    #     dbx.files_upload(open(f'{file_name}.png',"rb").read(),f'/{file_name}.png')
    #     return file_url
        
    def scrape_img_urls(self):     
        images_divs = self.soup.find_all("div", class_="owl-gallery__content")        
        images_urls = []
        if images_divs:
            for div in images_divs:
                try:
                    img = div.find("img")["src"]
                    print(img)
                    type(img)
                    images_urls.append(img)
                except:
                    pass

        formatted = []
        for img in set(images_urls):
            formatted.append({"url": img})
        return formatted

    def download_images_urls(self):
        images_urls = self.scrape_img_urls()


# pc = PreviewScraper()
# pc.scrape(listings_thumbnails)
