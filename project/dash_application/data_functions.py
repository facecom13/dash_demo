import os

import pandas as pd
import requests
import datetime
import re
import json
import shutil
from pathlib import Path


def move_css(theme_name):

    project_folder = Path(__file__).resolve().parent.parent
    assets_path_folder = str(project_folder) + '/assets'
    # итерируемся по списку и удаляем из assets если там что-то есть
    for filename in os.listdir(assets_path_folder):
        if 'bootswatch' in str(filename) or 'variables' in str(filename) or 'bootstrap' in str(filename):
            f = os.path.join(assets_path_folder, filename)
            os.remove(f)
    list_of_target_files = ['_bootswatch_', '_variables_', 'bootstrap_']
    bootswatch_source_file_path = str(project_folder) + '/datafiles/css_data/' + '_bootswatch_' + theme_name + '.scss'
    bootswatch_target_file_path = str(project_folder) + '/assets/' + '_bootswatch_' + theme_name + '.scss'
    shutil.copy(bootswatch_source_file_path, bootswatch_target_file_path)

    variables_source_file_path = str(project_folder) + '/datafiles/css_data/' + '_variables_' + theme_name + '.scss'
    variables_target_file_path = str(project_folder) + '/assets/' + '_variables_' + theme_name + '.scss'
    shutil.copy(variables_source_file_path, variables_target_file_path)

    bootstrap_source_file_path = str(project_folder) + '/datafiles/css_data/' + 'bootstrap_' + theme_name + '.css'
    bootstrap_target_file_path = str(project_folder) + '/assets/' + 'bootstrap_' + theme_name + '.css'
    shutil.copy(bootstrap_source_file_path, bootstrap_target_file_path)


# move_css('cerulean')