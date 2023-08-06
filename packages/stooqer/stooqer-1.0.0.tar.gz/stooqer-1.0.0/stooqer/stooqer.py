import requests
import io
from pandas import DataFrame, read_csv
import datetime

def to_date_str(date):
    if isinstance(date, datetime.datetime):
        return date.strftime("%Y%m%d")
    elif isinstance(date, str):
        return(date)

class Stock(DataFrame):
    
    def __init__(self, ticker, start = None, end = None, interval: str = 'y'):
        
        if end is not None:
            
            if start in None:
                raise ValueError('When passing "end" argument, "start" argument is required') #TODO Add first date aqusition method
            
            else:
                start = to_date_str(start)
                end = to_date_str(start)
                url = f'https://stooq.com/q/d/l/?s={ticker}&d1={start}&d2={end}1&i={interval}'
        
        elif start is not None:
            
            start = to_date_str(start)
            end = to_date_str(datetime.date.today())
            url = f'https://stooq.com/q/d/l/?s={ticker}&d1={start}&d2={end}1&i={interval}'

        else:
            url = f'https://stooq.com/q/d/l/?s={ticker}&i={interval}'
        
        response = requests.get(url)
        data = response.content.decode('utf-8')
        try:
            stock_data = read_csv(io.StringIO(data), index_col='Date', parse_dates=True)
        except ValueError:
            raise ValueError('Ticker is not valid, try with ".US" extension for US stocks')
        except:
            raise Exception('Unknown error. Might be caused by excesive use of stooq api')
        super().__init__(stock_data)