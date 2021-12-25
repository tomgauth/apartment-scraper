## apartment-scraper

This script is used to scrape listings from the website https://www.alberlet.hu/en/ and display them in an airtable. 


## Installation

1. Create a new Airtable base
2. Import the 'template.csv' file as a new table
3. Import the 'settings.csv' file as a new table
4. Download the app from github
5. Install the required dependencies using

```bash
pip install requirements.txt
```

6. Run the script
```bash
python main.py
```

## Usage

1. Fill in the "Settings" Table in your airtable. Give a name to the row (e.g: "basic")

1. You will be prompted to enter your:
- airtable api key
- airtable base name
- config  (the row name of your Settings row in airtable)

Run the script and see the listings appear in your airtable!


## License
[MIT](https://choosealicense.com/licenses/mit/)