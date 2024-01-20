from cgi import test
import pandas as pd
import math, numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

spolki = ['pko', 'mil']
okresy = ['Dzienne', 'Tygodniowe']
podstawowe_charakterystyki_spolek = pd.DataFrame(columns=['Spółka (kod)', 'Okres stóp wzrotu', 'Średnia',
                                                          'Odchylenie standardowe', 'Skośność', 'Kurtoza'])

testy_zgodnosci = pd.DataFrame(columns=['Spółka (kod)', 'Okres stóp wzrotu', 'Chi-kwadrat z rozkładem normalnym',
                                                          'Kolmogorova z rozkładem normalnym', 'Shapiro-Wilka z rozkładem normalnym',
                                                     'Chi-kwadrat z rozkładem t-studenta', 'Kolmogorova z rozkładem t-studenta'])

i = 0
j = 0
fig, axs = plt.subplots(2, 2)
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
        podstawowe_charakterystyki_spolek.loc[len(podstawowe_charakterystyki_spolek.index)] = [spolka.upper(), okres + ' stopy',
                                                                                               srednia, odchylenie_standardowe,
                                                                                               skosnosc, kurtoza]

        # Tworzenie histogramów
        axs[i, j].hist(dane['Stopa zwrotu'], bins=15)
        axs[i, j].set_title(label='(' + spolka.upper() + ') ' + okres + " stopy zwrotu akcji \n- rozkład wartości", fontsize=8)

        # Testy zgodności z rozkładem normalnym
        liczba_wierszy_tabeli = len(dane['Stopa zwrotu'])
        shapiro_stats, shapiro_p_value = scipy.stats.shapiro(dane['Stopa zwrotu'])
        # do poprawy test chi square
        chi_norm_stats, chi_norm_p_value = scipy.stats.chisquare(dane['Stopa zwrotu'])
        kolmogorov_norm_stats, kolmogorov_norm_p_value = scipy.stats.kstest(dane['Stopa zwrotu'], np.random.normal(srednia, odchylenie_standardowe, liczba_wierszy_tabeli))

        # Testy zgodności z rozkładem t-studenta
        # do poprawy test chi square
        chi_t_stats, chi_t_p_value = scipy.stats.chisquare(dane['Stopa zwrotu'])
        kolmogorov_t_stats, kolmogorov_t_p_value = scipy.stats.kstest(dane['Stopa zwrotu'], np.random.standard_t(liczba_wierszy_tabeli - 1, liczba_wierszy_tabeli))
        testy_zgodnosci.loc[len(testy_zgodnosci.index)] = [spolka.upper(),
                                                            okres + ' stopy',
                                                            '{:.5f}'.format(chi_norm_p_value),
                                                           '{:.5f}'.format(kolmogorov_norm_stats),
                                                            '{:.5f}'.format(shapiro_stats),
                                                           '{:.5f}'.format(chi_t_p_value),
                                                           '{:.5f}'.format(kolmogorov_t_p_value)]
        j = j + 1
    j = 0
    i = i + 1

# Wyświetlenie wykresu i zapisanie danych w plikach csv
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.show()

podstawowe_charakterystyki_spolek.to_csv('charakterystyki.csv')
testy_zgodnosci.to_csv('testy zgodności.csv')
