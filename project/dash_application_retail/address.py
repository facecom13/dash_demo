import xmltodict
import pandas as pd
from dadata import Dadata
import time
token = "6508c87623a6bad5dd0c9bb8e32897f7bfa14765"
secret = "aca80bbbff388090756278c3a275342f6fb16dfd"
dadata = Dadata(token, secret)

xml_data = open('data-20190925-5-structure-20160901.xml', 'r').read()  # Read data
xmlDict = xmltodict.parse(xml_data)  # Parse XML

list_of_items = xmlDict['Semenovodcheskie_hozyaystva']['items']
address_list = []
for item_dict in list_of_items:
    address = item_dict['Kontakty']['item']
    address_list.append(address)
# print(address_list[101])

# address_list = ['Москва ул. Мусоргского д9', 'Санкт-Петербург бульвар Новаторов д100']

address_df = pd.DataFrame()
i=0
for address in address_list:
    i=i+1
    print(i)
    result_list = []
    temp_dict = {}
    result = dadata.clean("address", address)
    time.sleep(4)
    geo_lat = result['geo_lat']
    try:
        geo_lat = float(geo_lat)
        geo_lon = result['geo_lon']

        temp_dict['address'] = address
        temp_dict['geo_lat'] = geo_lat
        temp_dict['geo_lon'] = geo_lon
        result_list.append(temp_dict)
        temp_df = pd.DataFrame(result_list)
        address_df = pd.concat([address_df, temp_df])
        address_df.to_csv('address.csv')
    except:
        pass


# print(address_df)


