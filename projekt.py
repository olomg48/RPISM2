import pandas as pd
import math, numpy as np
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

        #Tworzenie histogramów
        plt.hist(dane['Stopa zwrotu'], bins=15)
        plt.title('(' + spolka.upper() + ') ' + okres + " stopy zwrotu akcji - rozkład wartości")
        plt.show()

podstawowe_charakterystyki_spolek.to_csv('charakterystyki.csv')

