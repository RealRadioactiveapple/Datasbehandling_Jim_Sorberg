import pandas as pd

df = pd.read_csv("../data/AAPL_TIME_SERIES_INTRADAY_EXTENDED.csv")
print(df.head())


class StockDataLocal:
    """class nethod to get and proces local stock data"""

    def __init__(self, data_folder_path: str = "../data/") -> None:
        self._data_folder_path = data_folder_path

    def stock_dataframe(self, stockname: str) -> list:
        """
        returns lsit of two dataframs 1 for daily timeseries one for interdaly
        """
        stock_df_list = []

        for path_ending in ["_TIME_SERIES_DAILY.csv","_TIME_SERIES_INTRADAY_EXTENDED.csv"]:
            path = self._data_folder_path + stockname + path_ending
            
            stock = pd.read_csv(path, index_col=0, parse_dates=True)
            stock.index.rename("Date", inplace=True)

            stock_df_list.append(stock)

        return stock_df_list