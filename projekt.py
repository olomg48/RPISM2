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

#tygodniowa stopa zwrotu
pko['Tygodniowa stopa zwrotu'] = np.log(pko["Otwarcie"]) - np.log(pko['Otwarcie'].loc[(pko['Data']==pko['Data']-7)])

#Przesunięcie spowodowało wartość Nan w pierwszym wierszu - wypełniamy zerem
pko.fillna(0, inplace=True)

print(pko[['Data', 'Otwarcie','Tygodniowa stopa zwrotu', 'Zamkniecie','Stopa zwrotu', 'Stopa otwarcie-zamkniecie', 'Stopa zamkniecie-otwarcie']].head(30))