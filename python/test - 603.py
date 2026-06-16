import time
import csv
from collections import deque

def issquarefree_seq(s, ds_type):
    """
    Sprawdza, czy słowo jest bezkwadratowe.
    ds_type pozwala dostosować sprawdzanie do struktury danych.
    """
    n = len(s)
    for l in range(1, n // 2 + 1):
        for i in range(n - 2 * l + 1):
            if ds_type in ["string", "list"]:
                # Lista natywna i string obsługują szybki slicing pod spodem (w C)
                if s[i:i+l] == s[i+l:i+2*l]: 
                    return False
            elif ds_type == "deque":
                # Deque nie wspiera slicingu. Porównujemy manualnie (odczyt O(n) dla każdego elementu)
                is_square = True
                for j in range(l):
                    if s[i + j] != s[i + l + j]:
                        is_square = False
                        break
                if is_square:
                    return False
    return True

def run_experiment(alphabet, start_word, strategy="rightmost", ds="list", iters=20):
    # Inicjalizacja struktur na podstawie startowego słowa (które jest przekazane jako ciąg lub lista)
    if ds == "string":
        # Wymagamy, aby dla testu stringowego alphabet i start_word były stringami
        if isinstance(start_word, list):
            s = "".join(map(str, start_word))
            alphabet = [str(a) for a in alphabet]
        else:
            s = start_word
    elif ds == "list":
        s = list(start_word)
    elif ds == "deque":
        s = deque(start_word)

    start_time = time.perf_counter()
    
    insert_depths = [] # Lista do śledzenia odległości wstawienia (0 = wstawienie na końcu)

    for _ in range(iters):
        n = len(s)
        found = False
        
        if strategy == "rightmost":
            positions = range(n, -1, -1)
        else:
            positions = range(0, n + 1)
            
        for p in positions:
            for c in alphabet:
                if ds == "string":
                    # Niemutowalne - tworzymy nowy łańcuch
                    w = s[:p] + c + s[p:]
                    if issquarefree_seq(w, ds):
                        s = w
                        found = True
                        insert_depths.append(n - p) # n to stara długość, p to miejsce wstawienia
                        break
                elif ds == "list":
                    # Mutowalne - modyfikujemy w miejscu
                    s.insert(p, c)
                    if issquarefree_seq(s, ds):
                        found = True
                        insert_depths.append(n - p)
                        break
                    else:
                        s.pop(p) # Wycofujemy zmianę
                elif ds == "deque":
                    # Mutowalne - modyfikujemy w miejscu
                    s.insert(p, c)
                    if issquarefree_seq(s, ds):
                        found = True
                        insert_depths.append(n - p)
                        break
                    else:
                        del s[p] # Wycofujemy zmianę na liście dwukierunkowej

            if found:
                break
        if not found:
            break
            
    end_time = time.perf_counter()
    
    # Formatowanie wyniku do czytelnej postaci przed zwróceniem
    if ds in ["list", "deque"]:
        # Jeśli elementem są emotki (dłuższe stringi), łączymy je spacją dla czytelności.
        # W przeciwnym razie (pojedyncze znaki lub cyfry) łączymy bez spacji.
        if isinstance(s[0], str) and len(str(s[0])) > 1:
            final_seq = " ".join(map(str, s))
        else:
            final_seq = "".join(map(str, s))
    else:
        final_seq = s
        
    # Wyliczenie średniej głębokości (zabezpieczenie przed błędem dzielenia przez 0)
    avg_depth = sum(insert_depths) / len(insert_depths) if insert_depths else 0

    return end_time - start_time, len(s), final_seq, avg_depth

# Definicja scenariuszy (różne alfabety, typy i formy struktur)
experiments = [
    # --- TESTY STRING (BAZA) ---
    {"nazwa": "Znaki (String) - '123'", "alphabet": "123", "start": "1", "ds": "string"},
    
    # --- TESTY LIST (Zwykła tablica) ---
    {"nazwa": "Znaki (List) - ['a','b','c']", "alphabet": ['a', 'b', 'c'], "start": ['a'], "ds": "list"},
    {"nazwa": "Liczby int (List) - [1,2,3]", "alphabet": [1, 2, 3], "start": [1], "ds": "list"},
    {"nazwa": "ASCII Emotki (List)", "alphabet": [":-)", ":-D", "XD"], "start": [":-)"], "ds": "list"},
    {"nazwa": "Liczby int (List) - Start: [1,3]", "alphabet": [1, 2, 3], "start": [1, 3], "ds": "list"},
    
    # --- TESTY DEQUE (Lista dwukierunkowa) ---
    {"nazwa": "Znaki (Deque)", "alphabet": ['a', 'b', 'c'], "start": ['a'], "ds": "deque"},
    {"nazwa": "Liczby int (Deque)", "alphabet": [1, 2, 3], "start": [1], "ds": "deque"},
    {"nazwa": "ASCII Emotki (Deque)", "alphabet": [":-)", ":-D", "XD"], "start": [":-)"], "ds": "deque"}
]

results = []
stats_dict = {}

# Parametry globalne
ITERATIONS = 200
STRATEGY = "rightmost" # Poprawiona literówka

print("Trwa testowanie... (sprawdzanie `deque` może chwilę potrwać)")

for idx, exp in enumerate(experiments):
    exec_time, final_len, final_seq, avg_depth = run_experiment(
        alphabet=exp["alphabet"],
        start_word=exp["start"],
        strategy=STRATEGY,
        ds=exp["ds"],
        iters=ITERATIONS
    )
    
    res = {
        "id_testu": idx + 1,
        "nazwa_testu": exp["nazwa"],
        "typ_danych": type(exp["alphabet"][0]).__name__, # Pobiera nazwe typu: int, str
        "struktura_danych": exp["ds"],
        "iteracje": ITERATIONS,
        "dlugosc_koncowa": final_len,
        "srednia_glebokosc": round(avg_depth, 3), # <--- Zapisujemy średnią głębokość do słownika
        "czas_wykonania_sek": round(exec_time, 5),
        "wygenerowany_ciag": final_seq
    }
    results.append(res)
    
    # Zmodyfikowany wpis do słownika statystyk, by od razu pokazywał głębokość w konsoli
    stats_dict[exp["nazwa"]] = f"Czas: {round(exec_time, 4)} s | Średnia głębokość: {round(avg_depth, 3)}"

# Eksport do CSV
csv_filename = 'wyniki_eksperymentow_603.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Zapisano plik {csv_filename}!\n")

print("-" * 75)
print(f"STATYSTYKI CZASOWE I GŁĘBOKOŚCI ({ITERATIONS} iteracji) - podsumowanie:")
print("-" * 75)
for k, v in stats_dict.items():
    print(f"{k.ljust(35)} : {v}")