from pathlib import Path
import bigjson

def create_leasing_data_table_func(reload_leasing_table):
    output = 'test'
    if reload_leasing_table:
        project_folder = Path(__file__).resolve().parent.parent.parent
        # json_data = str(project_folder) + '/credit_demo_data.json'
        json_data_file = str(project_folder) + '/data.json'

        i = 0
        with open(json_data_file, 'rb') as f:
            j = bigjson.load(f)
        element = j[i]
        output = element['Контрагент']



        # output = 'pressed'
    return output