import requests
from datetime import datetime, date
import db_nomics_helpers as dbh

countries = ['ARG', 'AUS', 'AUT', 'BEL', 'BGR', 'BRA', 'CAN', 'CHE', 'CHL', 'CHN', 'COL', 'CRI', 'CZE', 'DEU', 'DNK', 'EA19', 'ESP', 'EST', 'EU15', 'EU27_2020', 'FIN', 'FRA', 'G', 'G', 'GBR', 'GRC', 'HRV', 'HUN', 'IDN', 'IND', 'IRL', 'ISL', 'ISR', 'ITA', 'JPN', 'KOR', 'LTU', 'LUX', 'LVA', 'MEX', 'NAFTA', 'NLD', 'NOR', 'NZL', 'OECD', 'OECDE', 'OTF', 'POL', 'PRT', 'ROU', 'RUS', 'SAU', 'SVK', 'SVN', 'SWE', 'TUR', 'USA', 'ZAF']
frequencies = ['A', 'Q']


for country in countries[:1]:
  for frequency in frequencies:
    try:
      dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      data = requests.get(f'https://api.db.nomics.world/v22/series/OECD/QNA?dimensions=%7B%22LOCATION%22%3A%5B%22{country}%22%5D%2C%22FREQUENCY%22%3A%5B%22{frequency}%22%5D%7D&observations=1')
      data_json = data.json()

      for i in range(len(data_json['series']['docs'])):
        dbh.insert_db_nomics_series(data_json['series']['docs'][i], data_json['provider'], dt_string)

    except:
      pass