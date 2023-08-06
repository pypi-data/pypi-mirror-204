import datetime

#TODO Dodać więcej formatów daty jeżeli będzie taka potrzeba
def to_date_str(date):
    if isinstance(date, datetime.datetime):
        return date.strftime("%Y%m%d")
    elif isinstance(date, str):
        return(date)
    
class bc:
    hd = '\033[95m'
    blu = '\033[94m'
    OKCYAN = '\033[96m'
    grn = '\033[92m'
    warn = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'
    bld = '\033[1m'
    UNDERLINE = '\033[4m'

