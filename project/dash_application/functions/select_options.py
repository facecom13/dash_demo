

def select_options_func(list_for_select_options):
    unique_list = set(list_for_select_options)
    options_dict = {}
    for item in unique_list:
        options_dict[item] = item
    return options_dict