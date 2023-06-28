from dash import dash_table

def data_table_dark(datatable_data_df):
    datatable_dark = dash_table.DataTable(
              id='activity_status_table',

              data=datatable_data_df.to_dict('records'),
              columns=[{"name": i, "id": i} for i in datatable_data_df.columns],
                page_size=1,

              # style_table={
              #     'height': '600px',
              #     'overflowX': 'auto',
              #     'overflowY': 'auto'
              # },
              style_header={
                  'backgroundColor': 'rgb(30, 30, 30)',
                  'color': 'white'
              },
              style_data={
                  'backgroundColor': 'rgb(50, 50, 50)',
                  'color': 'white'
              },
              # filter_action='native',
              sort_action="native",

              # fixed_rows={
              #     "headers": True,
              # },
              # style_header={
              #     # 'backgroundColor': 'rgb(210, 230, 230)',
              #     'color': 'black',
              #     'fontWeight': 'bold'
              # },
              # style_data={
              #     'whiteSpace': 'normal',
              #     'height': 'auto'},
              # style_cell={
              #     'textAlign': 'left',
              #     'minWidth': '180px', 'width': '180px',
              #     'maxWidth': '180px',
              #     'whiteSpace': 'normal',
              #     'textOverflow': 'ellipsis',
              #     'overflow': 'hidden'
              # },
              # export_format="csv"
          ),
    return datatable_dark