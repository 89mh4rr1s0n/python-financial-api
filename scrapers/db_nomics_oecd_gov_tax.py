import requests
from datetime import datetime, date
import db_nomics_helpers as dbh

countries = ['AUS', 'AUT', 'AVG_FEDERAL', 'AVG_UNITARY', 'BEL', 'CAN', 'CHE', 'CHL', 'COL', 'CRI', 'CZE', 'DEU', 'DNK', 'ESP', 'EST', 'FIN', 'FRA', 'GBR', 'GRC', 'HUN', 'IRL', 'ISL', 'ISR', 'ITA', 'JPN', 'KOR', 'LTU', 'LUX', 'LVA', 'MEX', 'NLD', 'NOR', 'NZL', 'OAVG', 'POL', 'PRT', 'SVK', 'SVN', 'SWE', 'TUR', 'USA' ]
gov_lev_elems = ['FED', 'LOCAL', 'NES', 'SOCSEC', 'STATE', 'SUPRA']


for country in countries[:1]:
  for gov_lev_elem in gov_lev_elems[:1]:
    try:
      dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      data = requests.get(f'https://api.db.nomics.world/v22/series/OECD/REV?dimensions=%7B%22COU%22%3A%5B%22{country}%22%5D%2C%22GOV%22%3A%5B%22{gov_lev_elem}%22%5D%7D&observations=1')
      data_json = data.json()

      for i in range(len(data_json['series']['docs'])):
        dbh.insert_db_nomics_series(data_json['series']['docs'][i], data_json['provider'], dt_string)

    except:
      pass