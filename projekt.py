from cgi import test
import pandas as pd
import math, numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt

spolki = ['pko', 'mil']
okresy = ['Dzienne', 'Tygodniowe']
podstawowe_charakterystyki_spolek = pd.DataFrame(columns=['spolka', 'okres', 'srednia', 'odchylenie', 'skosnosc', 'kurtoza'])

for spolka in spolki:
    for okres in okresy:
        dane = pd.read_csv(spolka + '_d.csv')
        dane['Data'] = pd.to_datetime(dane['Data'])
        # dodajemy Zamkniecie_wczoraj, czyli datę zamknięcia przesuniętą o jeden dzień do tyłu

        # liczymy dzienną stopę zwrotu
        dane['Stopa zwrotu'] = np.log(dane['Zamkniecie']) - np.log(dane['Zamkniecie'].shift(1))

        # stopa zwrotu od otwarcia do zamknięcia
        dane['Stopa otwarcie-zamkniecie'] = np.log(dane['Zamkniecie']) - np.log(dane['Otwarcie'])

        # stopa zwrotu od zamkniecia do otwarcia
        dane['Stopa zamkniecie-otwarcie'] = np.log(dane['Otwarcie'].shift(1)) - np.log(dane['Zamkniecie'])

        #Wyfiltrowanie pustych wierszy z kolumny 'Stopa zwrotu'
        dane = dane[dane['Stopa zwrotu'].notnull()]
          

        if okres == 'Tygodniowe':
            #testy tygodniowe
            chi2_tyg = scipy.stats.chisquare(dane['Stopa zwrotu'])
            kolmogorov_tyg = scipy.stats.kstest(dane['Stopa zwrotu'], scipy.stats.norm.cdf)
            shapiro_tyg = scipy.stats.shapiro(dane['Stopa zwrotu'])
        else:
            #testy dzienne
            chi2_dzie = scipy.stats.chisquare(dane['Stopa zwrotu'])
            kolmogorov_dzie = scipy.stats.kstest(dane['Stopa zwrotu'], scipy.stats.norm.cdf)
            shapiro1_dzie = scipy.stats.shapiro(dane['Stopa zwrotu'])


        dane.to_csv(spolka + '.csv')
        stopy_zwrotu = dane['Stopa zwrotu']

        #Przefiltrowanie tabeli dla tygodniowych cen akcji (daty tylko w środę)
        if okres == 'Tygodniowe':
            dane = dane[dane['Data'].dt.weekday == 2]

        #Obliczanie podstawowych charakterystyk
        srednia = np.mean(stopy_zwrotu)
        odchylenie_standardowe = np.std(stopy_zwrotu)
        skosnosc = stats.skew(stopy_zwrotu)
        kurtoza = stats.kurtosis(stopy_zwrotu)
        podstawowe_charakterystyki_spolek.loc[len(podstawowe_charakterystyki_spolek.index)] = [spolka.upper(), okres + ' stopy', srednia, odchylenie_standardowe, skosnosc, kurtoza]

#print(chi2_dzie,"\n",chi2_tyg,"\n",kolmogorov_dzie,"\n",kolmogorov_tyg,"\n",shapiro1_dzie,"\n",shapiro_tyg)