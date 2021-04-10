# %% [code] {"_kg_hide-input":true,"_kg_hide-output":true}
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 1000)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

def fix_percent(s):
    return float(str(s).strip('%').replace(',', '.')) / 100.0

# %% [code]
raw1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1estW9mkArIcK-vrTQsQ2CYcs-GWPjufg3x01qt1i5po/gviz/tq?tqx=out:csv&sheet=Atualizacoes')
raw1['date'] = pd.to_datetime(raw1['data_atualizacao'], format='%d/%m/%Y')

raw2 = pd.read_json('https://drive.google.com/uc?id=1-GXNPJ9IXFU2LXeoMOCcY9DGDwYdUeWo&export=download')
#raw2['ocupacao_urc'] = raw2['ocupacao_urc'].apply(fix_percent)
#raw2['descartados'] = raw2['descartados'].str.replace(r'\D+', '').astype('int')
raw2['obitos_suspeitos'] = 0

print("raw1.shape=", raw1.shape)
print("raw2.shape=", raw2.shape)

print(raw2.select_dtypes(include='object').info())

# %% [code]
raw = pd.concat([raw1, raw2])

raw.head()

# %% [code]
print(raw2.select_dtypes(include='object').tail(10))

# %% [code]
clean = pd.DataFrame()

# %% [code]
#clean['Date'] = pd.to_datetime(raw['data_atualizacao'].apply(lambda s: s + '/2020'), format='%d/%m/%Y')
#clean.tail()
clean['Date'] = raw['date'] #pd.to_datetime(raw['data_atualizacao'], format='%d/%m/%Y')

# %% [code]
clean['Confirmed'] = raw['confirmados']
clean['Deaths']    = raw['obitos_confirmados']
clean['Recovered'] = raw['recuperados']
clean['Active']     = raw['internacoes_confirmados']
clean['Notifications'] = raw['total_notificacoes']
clean['Negative']  = raw['descartados']
clean['UnderInvestigation'] = raw['suspeitos']
clean['UnderInvestigationDeaths'] = raw['obitos_suspeitos']

# %% [code]
clean['URCOccupancy'] = (raw['ocupacao_urc'].apply(fix_percent))

# %% [code]
#clean = clean[clean['Date'] <= '2020-12-09']
clean.dropna(subset=['Confirmed', 'Notifications'], inplace=True)

# %% [code]
clean = clean.sort_values(by='Date')
clean['NewCases'] = clean['Confirmed'] - clean['Confirmed'].shift(1)
clean['NewDeaths'] = clean['Deaths'] - clean['Deaths'].shift(1)
clean['NewNegative'] = clean['Negative'] - clean['Negative'].shift(1)
clean['NewNotifications'] = clean['Notifications'] - clean['Notifications'].shift(1)
clean['NewInvestigation'] = clean['UnderInvestigation'] - clean['UnderInvestigation'].shift(1)
clean['NewInvestigation'] = clean['UnderInvestigationDeaths'] - clean['UnderInvestigationDeaths'].shift(1)
clean['NegativeRate'] = clean['Negative'] / clean['Notifications']

# %% [code]
clean.tail(10)

# %% [code]
clean.describe()

# %% [code]
clean.info()

# %% [code]
clean.to_csv('covid-limeira-daily.csv',  index=False)

# %% [code]
