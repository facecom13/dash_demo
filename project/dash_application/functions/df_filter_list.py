

def df_filter_list_func(input_from_select, full_selector_list):
    """принимает то, что мы взяли из селекта и список полных значений этого селекта. И отдает результат в виде списка значение селекта"""
    result_select_list = []
    if input_from_select == None:
        result_select_list = full_selector_list

    elif len(input_from_select) == 0:
        result_select_list = full_selector_list

    elif len(input_from_select) > 0:
        result_select_list = input_from_select
    else:
        print("что-то странное в функции selector_content")
    return result_select_list