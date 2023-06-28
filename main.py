import os
import requests
import pprint
import json
import pandas as pd

TOKEN = 'a37062a36393726f3911dde489fe88e8'
headers = {
    'X-TrackerToken': f'{TOKEN}',
}

# response = requests.get('https://www.pivotaltracker.com/services/v5/my/activity', headers=headers)
response = requests.get('https://www.pivotaltracker.com/services/v5/projects/2615506/story_transitions', headers=headers)
json_list = response.json()
df = pd.DataFrame(json_list)
df.to_csv('df.csv', encoding='utf-8')
final = json.dumps(json_list, indent=2, ensure_ascii=False)
# Задача. Вывести список последних 3 изменений. В виде таблицы.

print(final)


