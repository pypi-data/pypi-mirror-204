"""
This module contains the objects related to 5paisa client

@author: Rathod Darshan
"""


import os as _os
import py5paisa as _p5
import pandas as _pd
import websocket as _ws
import datetime as _dtm
import json as _json
from websocket import create_connection as _create_connection
import websocket as _websocket
from py5paisa.order import Order as _Order
from typing import Union


from .utils import *

from ..stock_base import Stock


class ScripMaster:
    """ScripMaster contains all the scipts of 5paisa client.

    To get the name and symbol of any script, this class needs to be accessed. This class just filters the data from single .csv.
    """

    def __init__(self, filepath: str = None) -> None:
        """Initializes the ScripMaster class.

        Loads the .csv file into data attribute.

        Parameters
        ----------
        filepath : str, optional
            filepath to .csv file. If filepath is given then it reads the file, else it will download the file. by default None
        """
        if filepath is not None:
            self.data = _pd.read_csv(filepath,index_col=0)
        else:
            self.data = _pd.read_csv(
                "https://images.5paisa.com/website/scripmaster-csv-format.csv"
            )

        self.data["Expiry"] = _pd.to_datetime(
            self.data["Expiry"], format="%Y-%m-%d %H:%M:%S"
        )
        self.data["Name"] = self.data["Name"].apply(str.upper)
        self.data["Symbol"] = self.data["Name"]

    def __repr__(self):
        return f"scrip master data"

    def __call__(self):
        return self.data

    def save(self, filepath: str) -> None:
        """saves the scrip master data

        Parameters
        ----------
        filepath : str
            filepath with filename with .csv extention

        Returns
        -------
        _type_
            None
        """
        return self.data.to_csv(filepath)

    def get_scrip(self, stocklist: list[Stock]) -> _pd.DataFrame:
        """returns the scrips for list of stocks

        Parameters
        ----------
        stocklist : list[Stock]
            list of stocks

        Returns
        -------
        _pd.DataFrame
            Scrip data for given list of stocks.
        """
        ls1 = []
        for s1 in stocklist:
            try:
                ls1.append(s1.scrip)
            except:
                d1 = self.data
                f1 = (
                    (d1["Exch"] == s1.exchange)
                    & (d1["ExchType"] == s1.exchange_type)
                    & (d1["Symbol"] == s1.symbol)
                )
                f2 = (d1["Series"] == "EQ") | (d1["Series"] == "XX")
                d2 = d1[f1 & f2]
                if d2.empty:
                    raise ValueError(f"No Scrip found for {s1.symbol} in scrip_master")
                s1.scrip = d2.set_index("Name")
                ls1.append(s1.scrip)
        return _pd.concat(ls1)


class Client5paisa(_p5.FivePaisaClient):
    def __init__(
        self,
        email: str = None,
        password: str = None,
        dob: str = None,
        cred: dict = None,
        scrip_master: ScripMaster = None,
        login_using_token: bool = False,
    ) -> None:
        """Logs into the 5paisa client.

        Parameters
        ----------
        email : str
            registered email id of the user
        password : str
            password of the user
        dob : str
            date of birth in "YYYYMMDD" format
        cred : dict
            user developer API credentials. can be found on https://tradestation.5paisa.com/apidoc
            First login to 5paisa. And in menu -> Developer's API -> Get API keys. API credentials can be found.
        scrip_master : ScripMaster
            ScripMaster instance. This will be used for generating required inputs for various data fatching methods.
        login_using_token : bool
            If True then you have to go to URL and input the response URL. By default False.
        """
        if login_using_token:
            _p5.FivePaisaClient.__init__(self, cred=cred)
            print("go to this URL and input the response token")
            print(
                f'https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey={cred["USER_KEY"]}&ResponseURL=https://www.5paisa.com/technology/developer-apis'
            )
            str1 = input("input the whole URL after login here")
            token = str1.split("RequestToken=")[-1].split("&state")[0]
            self.get_access_token(token)
        else:
            _p5.FivePaisaClient.__init__(
                self, email=email, passwd=password, dob=dob, cred=cred
            )
            self.login()
            self.ws_feed = _create_connection(self._web_url1)

        self.scrip_master = scrip_master

    def __check_scrip_master(self) -> bool:
        """Checks if scrip_master is provided

        Returns
        -------
        bool
            True, if scrip_master is provided.

        Raises
        ------
        TypeError
            If scrip_master is None.
        """
        if self.scrip_master is None:
            raise TypeError(
                "scrip_master is None. Please provide ScripMaster instance."
            )
        else:
            return True

    def historical_data(
        self,
        Exch: str,
        ExchangeSegment: str,
        ScripCode: int,
        time: str,
        From: str,
        To: str,
    ) -> _pd.DataFrame:
        """Downloads the data.
        Returns
        -------
        _pd.DataFrame
            data
        """
        self.jwt_headers["x-clientcode"] = self.client_code
        self.jwt_headers["x-auth-token"] = self.Jwt_token
        url = f"{self.HISTORICAL_DATA_ROUTE}{Exch}/{ExchangeSegment}/{ScripCode}/{time}?from={From}&end={To}"
        timeList = ["1m", "5m", "10m", "15m", "30m", "60m", "1d"]
        if time not in timeList:
            return "Invalid Time Frame. it should be within [1m,5m,10m,15m,30m,60m,1d]."
        else:
            response = self.session.get(url, headers=self.jwt_headers).json()
            candleList = response["data"]["candles"]
            df = _pd.DataFrame(candleList)
            df.columns = ["Datetime", "Open", "High", "Low", "Close", "Volume"]
            df["Datetime"] = _pd.to_datetime(df["Datetime"])
            return df.set_index("Datetime")

    def download_historical_data(
        self,
        stocklist: list[Stock],
        interval: str = "1d",
        start: Union[str, _dtm.datetime] = "2023-01-01",
        end: Union[str, _dtm.datetime] = "2023-03-30",
    ) -> None:
        """Downloads the historical data and saves it to local drive or in Stock.data variable.

        Parameters
        ----------
        stocklist : list[Stock]
            list of Stocks
        interval : str, optional
            time interval of data. it should be within [1m,5m,10m,15m,30m,60m,1d], by default "1d"
        start : Union[str, _dtm.datetime], optional
            start date of the data. The data for this date will be downloaded, by default "2023-01-01"
        end : Union[str, _dtm.datetime], optional
            end date of the data. The data for this date will be downloaded, by default "2023-03-30"
        """
        self.__check_scrip_master()
        scrip = self.scrip_master.get_scrip(stocklist)

        if type(start) is not str:
            start = start.strftime("%Y-%m-%d")
        if type(end) is not str:
            end = end.strftime("%Y-%m-%d")

        for s1 in stocklist:
            print(s1.symbol)
            s1.save_historical_data(
                self.historical_data(
                    s1.exchange,
                    s1.exchange_type,
                    scrip.loc[s1.symbol, "Scripcode"],
                    interval,
                    start,
                    end,
                ),
                interval=interval,
            )

    @property
    def _web_url1(self):
        return f"wss://openfeed.5paisa.com/Feeds/api/chat?Value1={self.Jwt_token}|{self.client_code}"

    def get_market_depth(self, stocklist: list[Stock]) -> _pd.DataFrame:
        """Gets the market depth for given list of Stocks

        Parameters
        ----------
        stocklist : list[Stock]
            list of Stock class instances.

        Returns
        -------
        _pd.DataFrame
            Live Market Depth for all the Stocks in list.
        """
        a = _pd.DataFrame()
        for s1 in stocklist:
            a = _pd.concat([a, s1.scrip])
        syms = a["Symbol"].values
        a = a.rename(columns={"Exch": "Exchange", "ExchType": "ExchangeType"})[
            ["Exchange", "ExchangeType", "Symbol"]
        ].to_dict(orient="records")

        d1 = _pd.DataFrame(self.fetch_market_depth_by_symbol(a)["Data"])
        d1["Datetime"] = _dtm.datetime.now()
        d1["Symbol"] = syms
        return d1

    def get_market_feed(self, stocklist: list[Stock]) -> _pd.DataFrame:
        """Gets the market feed for given list of Stocks

        Parameters
        ----------
        stocklist : list[Stock]
            list of Stock class instances.

        Returns
        -------
        _pd.DataFrame
            Live Market Feed for all the Stocks in list.
        """
        a = _pd.DataFrame()
        for s1 in stocklist:
            a = _pd.concat([a, s1.scrip])
        a = a[["Exch", "ExchType", "Symbol"]].to_dict(orient="records")
        d1 = _pd.DataFrame(self.fetch_market_feed(a)["Data"])
        d1["Datetime"] = _dtm.datetime.now()
        return d1

    def get_market_data(
        self, stocklist: list[Stock], feed_type: str = "md"
    ) -> _pd.DataFrame:
        """Fetches the market data.

        The data fetched contains bid and offer qty and prices, depending upon the type of data requested.

        Parameters
        ----------
        stocklist : list[Stock]
            list of Stocks
        feed_type : str, optional
            'md' or 'mf'. 'md' gives 5 depth but not LTP. 'mf' gives only single depth and LTP., by default 'md'

        Returns
        -------
        _pd.DataFrame
            Data
        """
        a = _pd.DataFrame()
        for s1 in stocklist:
            a = _pd.concat([a, s1.scrip])
        a = a.rename(columns={"Scripcode": "ScripCode"})[
            ["Exch", "ExchType", "ScripCode"]
        ].to_dict(orient="records")
        mf_list = self.Request_Feed(feed_type, "s", a)

        self.ws_feed = _create_connection(self._web_url1)
        self.ws_feed.send(_json.dumps(mf_list))
        d1 = ""
        if feed_type == "md":
            for s in mf_list["MarketFeedData"]:
                d1 = d1 + ",{" + self.ws_feed.recv()[1:-1] + "}"
        if feed_type == "mf":
            for s in mf_list["MarketFeedData"]:
                d1 = d1 + "," + self.ws_feed.recv()[1:-1]
        self.ws_feed.close()
        d1 = "[" + d1[1:] + "]"
        return _pd.DataFrame(_json.loads(d1))

    def get_weekly_option_expiry(self) -> _pd.DataFrame:
        """gets the weekly option expiry from NIFTY.

        Returns
        -------
        _pd.DataFrame
            Option expiry dates
        """
        d1 = self.get_expiry("N", "NIFTY")
        d1 = _pd.DataFrame(d1["Expiry"])
        d1["Timestamp"] = d1["ExpiryDate"].apply(
            lambda x: int(x.split("+")[0].split("(")[-1])
        )
        d1["Date"] = d1["Timestamp"].apply(lambda x: _dtm.date.fromtimestamp(x // 1000))
        return d1

    def get_monthly_option_expiry(self) -> _pd.DataFrame:
        """gets the weekly option expiry from RELIANCE.

        Returns
        -------
        _pd.DataFrame
            Option expiry dates
        """
        d1 = self.get_expiry("N", "RELIANCE")
        d1 = _pd.DataFrame(d1["Expiry"])
        d1["Timestamp"] = d1["ExpiryDate"].apply(
            lambda x: int(x.split("+")[0].split("(")[-1])
        )
        d1["Date"] = d1["Timestamp"].apply(lambda x: _dtm.date.fromtimestamp(x // 1000))
        return d1

    def get_option_chain(
        self, stock: Stock, expiry_date: Union[str, _dtm.datetime]
    ) -> _pd.DataFrame:
        if type(expiry_date) is str:
            expiry_date = _dtm.datetime.strptime(expiry_date, "%Y-%m-%d").date()
        d1 = self.get_weekly_option_expiry()
        f1 = d1["Date"] == expiry_date
        ts = d1[f1]["Timestamp"].iloc[0]

        return _pd.DataFrame(super().get_option_chain(stock.exchange, stock.symbol, ts)['Options'])

