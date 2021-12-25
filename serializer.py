from pyairtable.formulas import match
from pyairtable import Table


class Serializer:

	def __init__(self, settings_table):
		self.settings_table = settings_table

	def airtable_to_search(self, config_name):
		config_data = self.settings_table.first(formula=match({"Config name":config_name}))
		data = config_data['fields']	
		formatted = {}	
		formatted['rental_fee_euro'] = f"400-{data['Price max']}-eur" or ''
		formatted['min_size'] = f"{data['Surface min']}" or ''
		formatted['room'] = f"{data['Num rooms min']}-x" or ''
		formatted['keyword'] = f"{data['Keyword']}" or ''
		return formatted


	def df_to_dict(self, df):
		dictionary = {}
		for row in df.iterrows():
			print("row: ", row)
			key = row[1][0]
			value = row[1][1]
			print(f'{key} -  {value}')
			dictionary[key] = value		
		return dictionary

