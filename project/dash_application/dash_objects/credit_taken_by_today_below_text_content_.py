import datetime
from dash import html
def credit_taken_by_today_below_text_content_func():
    today = datetime.datetime.now()
    current_year = today.year
    today_str = today.strftime('%d.%m.%Y')
    text_output = html.P(f'На {today_str} с начала {str(current_year)}г.')
    return text_output
