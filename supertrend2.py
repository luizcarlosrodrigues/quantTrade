'''
@author: Luiz Rodrigues
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#SuperTrend
def ST(df,f,n): #df is the dataframe, n is the period, f is the factor; f=3, n=7 are commonly used.
    #Calculation of ATR
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1)
    df['ATR']=np.nan
    df['ATR'].iloc[n-1]=df['TR'][:n-1].mean()
    for i in range(n,len(df)):
        df['ATR'][i]=(df['ATR'][i-1]*(n-1)+ df['TR'][i])/n

    #Calculation of SuperTrend
    df['Upper Basic']=(df['High']+df['Low'])/2+(f*df['ATR'])
    df['Lower Basic']=(df['High']+df['Low'])/2-(f*df['ATR'])
    df['Upper Band']=df['Upper Basic']
    df['Lower Band']=df['Lower Basic']
    
    for i in range(n,len(df)):
        if (df['Upper Basic'][i] < df['Upper Band'][i-1]) or (df['Close'][i-1] > df['Upper Band'][i-1]):
            df['Upper Band'][i] = df['Upper Basic'][i]
        else:
            df['Upper Band'][i] = df['Upper Band'][i-1]

        if (df['Lower Basic'][i] > df['Lower Band'][i-1]) or (df['Close'][i-1] < df['Lower Band'][i-1]):
            df['Lower Band'][i] = df['Lower Basic'][i]
        else:
            df['Lower Band'][i] = df['Lower Band'][i-1]    
        
    df['SuperTrend'] = df['Upper Band']
    df = df[df['SuperTrend'] > 0]

    for i in range(n,len(df)):
        if (df['SuperTrend'][i-1] == df['Upper Band'][i-1]) and (df['Close'][i] < df['Upper Band'][i]):
            df['SuperTrend'][i] = df['Upper Band'][i]
        elif (df['SuperTrend'][i-1] == df['Upper Band'][i-1]) and (df['Close'][i] > df['Upper Band'][i]):
            df['SuperTrend'][i] = df['Lower Band'][i]
        elif (df['SuperTrend'][i-1] == df['Lower Band'][i-1]) and (df['Close'][i] > df['Lower Band'][i]):
            df['SuperTrend'][i] = df['Lower Band'][i]
        elif (df['SuperTrend'][i-1] == df['Lower Band'][i-1]) and (df['Close'][i] < df['Lower Band'][i]):
            df['SuperTrend'][i] = df['Upper Band'][i]
        else:
            df['SuperTrend'][i] = 0
    
    df['Signal'] = df.apply(signal, axis=1)

    return df

def signal(c):
    if c['Close'] > c['SuperTrend']:
        return 'Buy'
    else:
        return 'Sell'