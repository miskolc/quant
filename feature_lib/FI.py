import pandas as pd

'''
Force Index(1) = {Close (current period)  -  Close (prior period)} x Volume
Force Index(13) = 13-period EMA of Force Index(1)
'''
# Force Index 
def ForceIndex(data, ndays): 
 FI = pd.Series(data['close'].diff(ndays) * data['volume'], name = 'fi') 
 data = data.join(FI) 
 return data
