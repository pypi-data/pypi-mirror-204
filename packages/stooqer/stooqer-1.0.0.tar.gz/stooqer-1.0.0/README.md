# Stooqer
Simple and light python class that allows for stock price download from stooq.com

## Usage
As of now, there is only one class that inherits from pandas DataFrame. Syntax for class usage is as follows:

```Python
aapl = Stock('aapl.us')
```

This will generate a pandas DataFrame object with stock data for AAPL

## Stock class

When creating class instance, user can pass arguments:

### Ticker (required)
A stock ticker name, sometimes requires to add a country directory for some stocks (like Apple, where it's needed to add .us). For more info about which ones require this directory, refer to stooq.com website

### Start (Optional*)
Start date for data download. Can be either a *string* (YYYYMMDD) or *datetime.datetime* object. If end argument is not given, the data will cover timeframe between start date and today

### End (Optional)
Similar to start argument, accepts strings and datetime.datetime objects. When passing end argument, the start argument needs to be specified as well - if not, the *ValueError* exception will be risen

### Interval (Optional / daily be default)
A data interval in a string format. Can be one of below; is daily be default:
- *y*: yearly
- *q*: quarterly
- *m*: monthly
- *d*: (default) daily

### Class variables
- *stock_name*: (string) stock ticker
- *ror*: (DataFrame) rate of return (simple, NOT LOG!) based on closing price
- *ror_avg*: (int) average rate of return (simple, NOT LOG!)
