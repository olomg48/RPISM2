import pandas as pd
import math, numpy as np
pko = pd.read_csv('pko_d.csv')
mil = pd.read_csv('mil_d.csv')

pko['Data'] = pd.to_datetime(pko['Data'])
#dodajemy Zamkniecie_wczoraj, czyli datę zamknięcia przesuniętą o jeden dzień do tyłu

#liczymy dzienną stopę zwrotu
pko['Stopa zwrotu'] = np.log(pko['Zamkniecie'].shift(1)) - np.log(pko['Zamkniecie'].shift(1))

#stopa zwrotu od otwarcia do zamknięcia
pko['Stopa otwarcie-zamkniecie'] = np.log(pko['Zamkniecie']) - np.log(pko['Otwarcie'])

#stopa zwrotu od zamkniecia do otwarcia
pko['Stopa zamkniecie-otwarcie'] = np.log(pko['Otwarcie'].shift(1)) - np.log(pko['Zamkniecie'])

# Tutaj przeprowadzane jest mapowanie, które umożliwi dodanie kolumny z zamknięciem sprzed tygodnia
data_map = {}
for i in range(len(pko)):
    current_date = pko.iloc[i]['Data']
    week_ago = current_date - pd.DateOffset(days=7)
    # Sprawdzenie, czy data sprzed tygodnia istnieje w danych
    data_map[current_date] = week_ago if week_ago in pko['Data'].values else pd.NaT

# Utworzenie nowej kolumny z wartością zamknięcia sprzed tygodnia lub NaN
pko['Zamkniecie tydzien temu'] = pko['Data'].map(data_map).map(pko.set_index('Data')['Zamkniecie'])

pko['Tygodniowa stopa zwrotu'] = np.log(pko['Zamkniecie']) - np.log(pko['Zamkniecie tydzien temu'])

# Wypełniamy wszystkie NaN zerami // nie wiem w sumie czy wypełniać, czy nie
#pko.fillna(0, inplace=True)


print(pko.head(30))




#print(pko[['Data', 'Otwarcie','Tygodniowa stopa zwrotu', 'Zamkniecie','Stopa zwrotu', 'Stopa otwarcie-zamkniecie', 'Stopa zamkniecie-otwarcie']].head(30))