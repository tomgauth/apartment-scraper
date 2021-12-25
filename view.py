

class MainView:

	def welcome(self):
		print("Welcome to the scraper >> ")

	def set_airtable_api(self):
		airtable_api = input("Paste the airtable api here >> ")
		return airtable_api

	def set_airtable_base(self):
		airtable_base = input("Paste the airtable base here >> ")
		return airtable_base

	def set_config_name(self):
		config_name = input("What search settings are you using? >> ")
		return config_name