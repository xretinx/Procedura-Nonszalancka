import os
import glob
import pandas as pd

def analizuj_pliki_csv(sciezka_folderu="."):
    # Wyszukiwanie wszystkich plików CSV w podanym folderze
    wzorzec = os.path.join(sciezka_folderu, "*_Prime_Wariant*.csv")
    pliki = glob.glob(wzorzec)
    
    if not pliki:
        print("Nie znaleziono odpowiednich plików CSV w podanym folderze.")
        return

    wyniki = []

    for sciezka_pliku in pliki:
        nazwa_pliku = os.path.basename(sciezka_pliku)
        
        # Inicjalizacja zmiennych domyślnych
        czas_wykonania = None
        status = "Nieznany"
        liczba_krokow = 0
        
        # Wyciągamy informacje o Wariancie z nazwy pliku
        wariant = "A" if "WariantA" in nazwa_pliku else "B" if "WariantB" in nazwa_pliku else "Nieznany"
        # Wyciągamy timestamp z nazwy pliku dla lepszej identyfikacji
        timestamp = nazwa_pliku.split('_Prime_')[0] if '_Prime_' in nazwa_pliku else "Nieznany"

        try:
            # 1. Odczyt metadanych (status i czas) na końcu pliku
            with open(sciezka_pliku, 'r', encoding='utf-8') as f:
                linie = f.readlines()
                for linia in linie:
                    if "Status zakonczenia:" in linia:
                        status = linia.split(',')[1].strip().replace('"', '')
                    elif "Czas wykonania (s):" in linia:
                        try:
                            czas_wykonania = float(linia.split(',')[1].strip())
                        except ValueError:
                            pass

            # 2. Odczyt liczby kroków (pomijamy metadane na dole za pomocą tail/dropna)
            # Używamy sep=',' oraz ignorujemy błędy wierszy z metadanymi
            df = pd.read_csv(sciezka_pliku, skiprows=1, sep=',', skipfooter=3, engine='python')
            # Filtrujemy tylko wiersze, gdzie Krok jest liczbą
            df['Krok'] = pd.to_numeric(df['Krok'], errors='coerce')
            df = df.dropna(subset=['Krok'])
            liczba_krokow = int(df['Krok'].max()) if not df.empty else 0

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {nazwa_pliku}: {e}")
            continue

        wyniki.append({
            "Plik": nazwa_pliku,
            "Timestamp": timestamp,
            "Wariant": wariant,
            "Liczba kroków": liczba_krokow,
            "Status": status,
            "Czas (s)": czas_wykonania
        })

    # Konwersja do DataFrame w celu łatwego podsumowania
    df_wyniki = pd.DataFrame(wyniki)
    
    print("\n" + "="*45 + " ZESTAWIENIE SZCZEGÓŁOWE " + "="*45)
    print(df_wyniki.to_string(index=False))
    print("="*115 + "\n")

    # Podsumowanie statystyczne
    print("="*20 + " PODSUMOWANIE METRYK " + "="*20)
    
    # 1. Ile ukończonych sukcesem (Wariant A), a ile uderzyło w limit (Wariant B)
    status_counts = df_wyniki['Status'].value_counts()
    print("\nStatystyka statusów zakończenia:")
    for stat, count in status_counts.items():
        print(f" - {stat}: {count} uruchomienie/a")

    # 2. Średni czas wykonania dla poszczególnych wariantów
    print("\nŚredni czas wykonania dla wariantów:")
    sredni_czas = df_wyniki.groupby('Wariant')['Czas (s)'].mean()
    for war, czas in sredni_czas.items():
        print(f" - Wariant {war}: {czas:.7f} sekund")
        
    print("="*63)

if __name__ == "__main__":
    # Skrypt domyślnie szuka plików w katalogu, w którym został uruchomiony
    analizuj_pliki_csv()