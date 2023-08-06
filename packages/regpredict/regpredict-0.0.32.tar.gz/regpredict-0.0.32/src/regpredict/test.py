import pandas as pd
from regbot import signal
#from regpredict.regbot import signal
df = pd.read_csv('../jupyter/regbot_v31_validation.csv')

y_pred = []
def getSignal(vol,rsi_5,rsi_15,sma_5,sma_7,sma_25,vc_grad):
    return 0 if signal(vol,rsi_5,rsi_15,sma_5,sma_7,sma_25,vc_grad) < 0.5 else 1


df = df[df['enter_long'] == 1]
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['volume'],row['rsi-05'],row['rsi-15'],row['sma-05'],row['sma-07'],row['sma-25'],row['vc-grad'] ), axis=1)

print(df.head())

print(len(df[df['result'] == df['enter_long']]), len(df))
