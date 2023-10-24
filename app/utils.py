import pytz

def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)

def get_type_ce(strike, atmStrike):
    if strike == atmStrike:
        return 'ATM'
    elif atmStrike < strike:
        return 'OTM'
    else:
        return 'ITM'

def get_type_pe(strike, atmStrike):
    if strike == atmStrike:
        return 'ATM'
    elif atmStrike > strike:
        return 'OTM'
    else:
        return 'ITM'

intz = pytz.timezone('Asia/Kolkata')