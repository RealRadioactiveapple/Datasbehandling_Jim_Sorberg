from logging import debug
from dash.dcc.Markdown import Markdown
import pandas as pd
import dash
from dash import dcc, html
from load_data import StockDataLocal
from dash.dependencies import Output, Input
import plotly_express as px
from time_filtering import filter_time

stock_data_objekt = StockDataLocal()
symbol_dict = dict(AAPL="Apple",NVDA="Nvidia", TSLA = "Tesla", IBM = "IBM")

stock_options_dropdown=[{"label":name, "value": symbol}
                        for symbol, name in symbol_dict.items()]


df_dict = {symbol: stock_data_objekt.stock_dataframe(symbol)
    for symbol in symbol_dict}

#ohlc options - open high low close

ohlc_options = [{"label":option.capitalize(), "value":option} for option in ["open","high","low", "close"]]

slider_marks = {i: mark for i, mark in enumerate(
    ["1 day", "1 week", "1 month", "3 months", "1 year", "5 years", "Max"]

) }



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("stocks viewer"),
    html.P("Choose a stock"),
    dcc.Dropdown(id='stock-picker-dropdown', className='',
        options=stock_options_dropdown,
        value='AAPL'
        ),

    html.P(id="highest-value"),
    html.P(id="lowest-value"),
    dcc.RadioItems(id ="ohlc-radio", className='',
                    options= ohlc_options,
                    value='close'
                    ),
    dcc.Graph(id="stock-graph",className=""),

    dcc.Slider(id='time-slider', className='', min=0, max=6, step=None, value= 2, marks= slider_marks),
    dcc.Store(id="filtered-df")
    

])
@app.callback(Output("filtered-df", "data"),
    Input("stock-picker-dropdown", "value"),
    Input("time-slider", "value"))

def filter_df(stock, time_index):
    """filters the dataframe storse in intermidery for callbacks 
    retunrs a json object of filter dataframe
    """
    dff_daily, dff_intraday = df_dict[stock]

    dff = dff_intraday if time_index <= 2 else dff_daily

    #maps 0-6 to number of days
    days = {i:day for i, day in enumerate([1,7,30,90,365,365*5])}

    dff = dff if time_index == 6 else filter_time(dff, days [time_index])

    return dff.to_json()


@app.callback(
    Output("stock-graph","figure"),
    Input("filtered-df", "data"),
    Input("stock-picker-dropdown","value"),
    Input("ohlc-radio", "value")
)







def update_graph(json_df, stock, ohlc):

    dff = pd.read_json(json_df)
    fig = px.line(dff, x = dff.index, y=ohlc, title= symbol_dict[stock])

    return fig # fig object goes in to Output ie figure property

@app.callback(
    Output("highest-value", "children"),
    Output("lowest-value", "children"),
    Input("filtered-df","data"),
    Input("ohlc-radio","value")
)

def higest_lowest_value(json_df, ohlc):

    dff = pd.read_json(json_df)
    highest_value = f"{dff[ohlc].max():.2f} USD"
    lowest_value = f"{dff[ohlc].min():.2f} USD"

    return highest_value, lowest_value


if __name__ == "__main__":
    app.run_server(debug=True)