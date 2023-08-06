"""Module consisting of base class of stock
"""

import os as _os
import datetime as _dtm
import numpy as _np
import pandas as _pd

from .utils import *

from typing import TypeVar, Union


class Stock:
    def __init__(
        self,
        symbol: str,
        exchange: str = "N",
        exchange_type: str = "C",
        store_local: bool = False,
        local_data_foldpath: str = None,
    ) -> None:
        """Manages the data for list of stocks.

        Parameters
        ----------
        Parameters
        ----------
        symbol : str
            Stock symbol as available online.
        exchange : str
            Stock Exchange. can be N, B, M for Nifty, BSE and MCX respectively. By default N
        exchange_type : str
            Type of Stock Exchange. can be C, D or U for Cash, Derivative or Currency respectively. By default C.
        store_local : bool, optional
            whether to store the historical or any downloaded data to local directory, by default True
        local_data_foldpath : str, optional
            path to folder where local data will be stored. Inside this folder, multiple folders of individual stocks are created and inside that stock folder, historical data and other data is stored. If None then path returned by _os.getcwd() is used, given that store_local is True. by default None
        """
        self.symbol = symbol
        if exchange in ["N", "B", "M"]:
            self.exchange = exchange
        else:
            raise ValueError(
                'exchange can be only "N" for Nifty, "B" for BSE or "M" for MCX, in Upper case.'
            )

        if exchange_type in ["C", "D", "U"]:
            self.exchange_type = exchange_type
        else:
            raise ValueError(
                'exchange_type can be only "C" for Cash or "D" for Derivative, in Upper case.'
            )

        self.foldname = self.exchange + "_" + self.exchange_type + "_" + self.symbol
        self.store_local = store_local
        if self.store_local:
            if local_data_foldpath is not None:
                self.local_data_foldpath = _os.path.join(
                    local_data_foldpath, self.foldname
                )
            else:
                self.local_data_foldpath = _os.path.join(_os.getcwd(), self.foldname)
            make_dir(self.local_data_foldpath)

    def __repr__(self):
        return f'{self.symbol} stock class'
    
    def save_historical_data(self, data: _pd.DataFrame, interval: str,) -> None:
        """saves the historical stock data.

        Multiple files, each for saparate month data is created.

        Parameters
        ----------
        data : _pd.DataFrame
            Data to be saved.
        interval : str
            time interval of the data
        """
        self.data = data

        if self.store_local is False:
            return

        start_time = data.index[0]
        end_time = data.index[-1]

        for y in range(start_time.year, end_time.year + 1):
            f1 = data.index.year == y
            data1 = data[f1]
            st1 = data1.index[0]
            se1 = data1.index[-1]
            for m in range(st1.month, se1.month + 1):
                f1 = data1.index.month == m
                data2 = data1[f1]
                filename = f"{y}{str(m).zfill(2)}_{interval}.pickle"
                filepath = _os.path.join(self.local_data_foldpath, filename)
                append_it(data2, filepath=filepath)
        return

    def load_historical_data(
        self,
        interval: str,
        start: Union[str, _dtm.datetime],
        end: Union[str, _dtm.datetime],
    ) -> _pd.DataFrame:
        """Loads the data from local_directory

        Parameters
        ----------
        interval : str
            time interval of data. it should be within [1m,5m,10m,15m,30m,60m,1d]
        start : Union[str, _dtm.datetime]
            start date of the data. The data for this date will be downloaded
        end : Union[str, _dtm.datetime]
            end date of the data. The data for this date will be downloaded

        Returns
        -------
        _pd.DataFrame
            data

        Raises
        ------
        ValueError
            if no data is found
        """

        if type(start) is str:
            start = _dtm.datetime.strptime(start, "%Y-%m-%d")
        if type(end) is str:
            end = _dtm.datetime.strptime(end, "%Y-%m-%d")

        ### converting the date to specific integer for comparision
        start_val = start.year * 100 + start.month
        end_val = end.year * 100 + end.month
        ### data of each month will be stored here
        datas = []
        ### the value of each month will be stored. This is done to sort the data in ascending order. Sorting can be performed here directly instead over the large dataframe.
        dates = []
        files = get_file_name(self.local_data_foldpath)
        for fname in files:
            if interval in fname:
                nm = fname.split("_")
                dt1 = _dtm.datetime.strptime(nm[0], "%Y%m")
                dt_val = dt1.year * 100 + dt1.month
                ### if this integer lies between the start and end date integer then read this file.
                if (dt_val >= start_val) and (dt_val <= end_val):
                    datas.append(
                        _pd.read_pickle(_os.path.join(self.local_data_foldpath, fname))
                    )
                    dates.append(dt_val)
        
        if dates == []:
            raise ValueError('No data found in given time period or time frame')
        
        ### sorting and concatenating
        dates = _np.array(dates)
        idx = _np.argsort(dates)
        ans = _pd.DataFrame()
        for i in idx:
            ans = _pd.concat([ans, datas[i]])

        ### after this the data will be filtered with date
        f1 = (ans.index.date >= start.date()) & (ans.index.date <= end.date())
        return ans[f1]

    @property
    def scrip_filepath(self) -> str:
        """filepath of scrip

        Returns
        -------
        str
            filepath
        """
        return _os.path.join(self.local_data_foldpath, "scrip.pickle")

    @property
    def scrip(self) -> _pd.DataFrame:
        """scrip for client 5paisa.

        Returns
        -------
        _pd.DataFrame
            scrip data.
        """
        return _pd.read_pickle(self.scrip_filepath)

    @scrip.setter
    def scrip(self, data: _pd.DataFrame) -> None:
        """saves the scrip

        Parameters
        ----------
        data : _pd.DataFrame
            scrip data. This can be optained by ScripMaster.get_scrip() method.
        """
        if self.store_local:
            data.to_pickle(self.scrip_filepath)
        return

