import time
import random
import matplotlib.pyplot as plt
from collections import Counter

def issquarefree_seq(s):
    n = len(s)
    for l in range(1, n // 2 + 1):
        for i in range(n - 2 * l + 1):
            if s[i:i+l] == s[i+l:i+2*l]: 
                return False
    return True

def run_experiment(name, start_word="1", alphabet="123", char_strategy="seq", iters=200):
    s = start_word
    insert_depths = []
    used_chars = []
    
    start_time = time.perf_counter()
    
    for iter_num in range(iters):
        n = len(s)
        found = False
        positions = range(n, -1, -1) # Priorytet pozycji (wstawianie od prawej)
        
        for p in positions:
            # Określenie strategii wyboru znaków
            current_alphabet = list(alphabet)
            if char_strategy == "random":
                random.shuffle(current_alphabet) # Mieszamy alfabet dla każdej sprawdzanej pozycji
                
            for c in current_alphabet:
                w = s[:p] + c + s[p:]
                if issquarefree_seq(w):
                    s = w
                    insert_depths.append(n - p) # Zapisujemy odległość od końca
                    used_chars.append(c)
                    found = True
                    break
            if found: break
        if not found: break
            
    end_time = time.perf_counter()
    
    # Zliczanie wystąpień znaków
    char_counts = dict(Counter(used_chars))
    for a in alphabet:
        if a not in char_counts: char_counts[a] = 0
            
    return {
        "nazwa": name,
        "czas": end_time - start_time,
        "glebokosci": insert_depths,
        "rozklad": char_counts,
        "wygenerowane_slowo": s
    }

# --- DEFINICJA SCENARIUSZY BADAWCZYCH ---
scenariusze = [
    {"nazwa": "Baza (Start '1', Alfabet '123', Sekwencyjnie)", "start": "1", "alfabet": "123", "strat": "seq"},
    {"nazwa": "Losowość (Start '1', Alfabet '123', Losowo)", "start": "1", "alfabet": "123", "strat": "random"},
    {"nazwa": "Duży alfabet (Start '1', Alfabet '12345', Sekwencyjnie)", "start": "1", "alfabet": "12345", "strat": "seq"},
    {"nazwa": "Inny Start (Start '12312', Alfabet '123', Sekwencyjnie)", "start": "12312", "alfabet": "123", "strat": "seq"}
]

wyniki = []
print("Trwa generowanie danych dla scenariuszy...")
for sc in scenariusze:
    res = run_experiment(sc["nazwa"], sc["start"], sc["alfabet"], sc["strat"], iters=200)
    wyniki.append((sc, res))

# --- GENEROWANIE WYKRESÓW ---
fig, axs = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("Analiza Procedury Nonszalanckiej - Wpływ alfabetu, słowa startowego i losowości", fontsize=16)

kolory = ['blue', 'green', 'purple', 'orange']

# Wykres 1: Głębokość wstawiania w czasie
for idx, (sc, res) in enumerate(wyniki):
    axs[0, 0].scatter(range(len(res["glebokosci"])), res["glebokosci"], 
                      label=sc["nazwa"], color=kolory[idx], alpha=0.6, s=15)
axs[0, 0].set_title("Odległość wstawienia od końca w kolejnych iteracjach")
axs[0, 0].set_xlabel("Numer iteracji")
axs[0, 0].set_ylabel("Głębokość (0 = na samym końcu)")
axs[0, 0].legend(fontsize=8)
axs[0, 0].grid(True, linestyle="--", alpha=0.5)

# Wykres 2, 3, 4: Rozkłady znaków (Bar charts)
# Aby wykresy były czytelne, narysujemy rozkład dla 3 wybranych eksperymentów obok siebie
baza_res = wyniki[0][1]["rozklad"]
los_res = wyniki[1][1]["rozklad"]
duzy_res = wyniki[2][1]["rozklad"]

axs[0, 1].bar(baza_res.keys(), baza_res.values(), color='blue', alpha=0.7)
axs[0, 1].set_title("Rozkład znaków - Algorytm Bazowy (Sekwencyjny)")
axs[0, 1].set_ylabel("Liczba wystąpień")

axs[1, 0].bar(los_res.keys(), los_res.values(), color='green', alpha=0.7)
axs[1, 0].set_title("Rozkład znaków - Wybór Losowy")
axs[1, 0].set_ylabel("Liczba wystąpień")

axs[1, 1].bar(duzy_res.keys(), duzy_res.values(), color='purple', alpha=0.7)
axs[1, 1].set_title("Rozkład znaków - Alfabet 5-znakowy")
axs[1, 1].set_ylabel("Liczba wystąpień")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("analiza_rozkładu_i_głębokości.png", dpi=300)
print("✅ Wykresy zapisano do pliku 'analiza_rozkładu_i_głębokości.png'")
plt.show()