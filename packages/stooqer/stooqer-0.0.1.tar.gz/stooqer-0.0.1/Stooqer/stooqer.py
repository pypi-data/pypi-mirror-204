import requests
import io
from pandas import DataFrame, read_csv
from parsing import to_date_str, bc
import datetime

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
        stock_data = read_csv(io.StringIO(data), index_col='Date', parse_dates=True)
        super().__init__(stock_data)

        #VARIABLES
        self.stock_name = ticker
        self.ror = self['Close'].pct_change()
        self.ror_avg = self.ror.mean()

    '''
    def summary(self, column: str = 'Close'): #TODO Dokończyć
        print(f'{bc.hd}///////////////SUMMARY {self.stock_name}/////////////////{bc.end}\n'
              f'{bc.blu}{bc.bld}Average rate of return: {bc.end}{bc.grn}{self[column].pct_change().mean()}{bc.end}\n'
              f'')
        
        def to_csv(column): #TODO Dodać eksport do CSV
            pass
    '''

#https://stooq.pl/q/d/l/?s=cdr&d1=19950802&d2=20230721&i=q
#https://stooq.pl/q/d/l/?s=cdr&i=q
#https://stooq.com/q/d/l/?s=cdr&i=q