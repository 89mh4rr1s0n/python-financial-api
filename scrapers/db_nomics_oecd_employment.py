import requests
from datetime import datetime, date
import db_nomics_helpers as dbh

countries = ['AUS','AUT','BEL','BRA','CAN','CHE','CHL','COL','CRI','CZE','DEU','DNK','EA19','ESP','EST','EU27_2020','EU28','FIN','FRA','G','GBR','GRC','HUN','IRL','ISL','ISR','ITA','JPN','KOR','LTU','LUX','LVA','MEX','NLD','NOR','NZL','OECD','POL','PRT','RUS','SVK','SVN','SWE','TUR','USA']

for country in countries[:1]:
    try:
      dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      data = requests.get(f'https://api.db.nomics.world/v22/series/OECD/ALFS_EMP?dimensions=%7B%22LOCATION%22%3A%5B%22{country}%22%5D%7D&observations=1')
      data_json = data.json()

      for i in range(len(data_json['series']['docs'])):
        dbh.insert_db_nomics_series(data_json['series']['docs'][i], data_json['provider'], dt_string)

    except:
      pass