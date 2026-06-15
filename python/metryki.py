import time
import matplotlib.pyplot as plt

def issquarefree_seq(s):
    n = len(s)
    for l in range(1, n // 2 + 1):
        for i in range(n - 2 * l + 1):
            if s[i:i+l] == s[i+l:i+2*l]: 
                return False
    return True

def run_advanced_diagnostic(strategy_type="pos_first", iters=200):
    s = "1"
    alphabet = "123"
    
    # Zmienne globalne dla podsumowania
    total_calls = 0
    used_chars = {'1': 0, '2': 0, '3': 0}
    
    # Listy do wykresów (dane zbierane per iteracja)
    calls_per_iteration = []
    cumulative_calls = []
    insert_depths = []
    
    start_time = time.perf_counter()
    
    for iter_num in range(iters):
        n = len(s)
        found = False
        positions = range(n, -1, -1)
        calls_this_iter = 0
        
        if strategy_type == "pos_first":
            for p in positions:
                for c in alphabet:
                    calls_this_iter += 1
                    total_calls += 1
                    w = s[:p] + c + s[p:]
                    if issquarefree_seq(w):
                        s = w
                        insert_depths.append(n - p) 
                        used_chars[c] += 1
                        found = True
                        break
                if found: break
                
        elif strategy_type == "char_first":
            for c in alphabet:
                for p in positions:
                    calls_this_iter += 1
                    total_calls += 1
                    w = s[:p] + c + s[p:]
                    if issquarefree_seq(w):
                        s = w
                        insert_depths.append(n - p)
                        used_chars[c] += 1
                        found = True
                        break
                if found: break
                
        if not found: 
            break
            
        # Zapis danych z tej iteracji
        calls_per_iteration.append(calls_this_iter)
        cumulative_calls.append(total_calls)
            
    end_time = time.perf_counter()
    
    return {
        "nazwa": strategy_type,
        "czas": end_time - start_time,
        "calkowite_wywolania": total_calls,
        "wywolania_per_iter": calls_per_iteration,
        "skumulowane_wywolania": cumulative_calls,
        "glebokosci": insert_depths,
        "rozklad_znakow": used_chars
    }

# --- 1. WYKONANIE BADAŃ ---
print("Uruchamiam zaawansowaną diagnostykę (200 iteracji)...")
res_pos = run_advanced_diagnostic("pos_first")
res_char = run_advanced_diagnostic("char_first")
print("Obliczenia zakończone. Generuję wykresy...")

# --- 2. GENEROWANIE WYKRESÓW DO DOKUMENTACJI ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Analiza porównawcza strategii tworzenia słowa bezkwadratowego (200 iteracji)", fontsize=16)

# Wykres 1: Liczba wywołań w każdej iteracji
axs[0, 0].plot(res_pos["wywolania_per_iter"], label="Pozycja priorytetem (Wersja A332603)", color="blue", alpha=0.7)
axs[0, 0].plot(res_char["wywolania_per_iter"], label="Alfabet priorytetem (Wersja A357436)", color="red", alpha=0.7)
axs[0, 0].set_title("Złożoność każdej iteracji (ile razy sprawdzano ciąg)")
axs[0, 0].set_xlabel("Numer iteracji")
axs[0, 0].set_ylabel("Liczba wywołań funkcji sprawdzającej")
axs[0, 0].legend()
axs[0, 0].grid(True, linestyle="--", alpha=0.5)

# Wykres 2: Skumulowana liczba wywołań (Narastająco)
axs[0, 1].plot(res_pos["skumulowane_wywolania"], label="Wersja 1", color="blue", linewidth=2)
axs[0, 1].plot(res_char["skumulowane_wywolania"], label="Wersja 2", color="red", linewidth=2)
axs[0, 1].set_title("Wzrost kosztu obliczeniowego w czasie")
axs[0, 1].set_xlabel("Rozmiar słowa (numer iteracji)")
axs[0, 1].set_ylabel("Skumulowana liczba wywołań")
axs[0, 1].legend()
axs[0, 1].grid(True, linestyle="--", alpha=0.5)

# Wykres 3: Rozkład głębokości wstawiania (Scatter plot)
axs[1, 0].scatter(range(len(res_pos["glebokosci"])), res_pos["glebokosci"], color="blue", label="Wersja 1", alpha=0.5, s=20)
axs[1, 0].scatter(range(len(res_char["glebokosci"])), res_char["glebokosci"], color="red", label="Wersja 2", alpha=0.5, marker="x")
axs[1, 0].set_title("Głębokość wstawiania nowego znaku")
axs[1, 0].set_xlabel("Numer iteracji")
axs[1, 0].set_ylabel("Odległość wstawienia od końca słowa (0 = na końcu)")
axs[1, 0].legend()
axs[1, 0].grid(True, linestyle="--", alpha=0.5)

# Wykres 4: Zestawienie całkowitych wywołań (Skala logarytmiczna)
labels = ['Wersja 1 (Pozycja)', 'Wersja 2 (Alfabet)']
values = [res_pos["calkowite_wywolania"], res_char["calkowite_wywolania"]]
bars = axs[1, 1].bar(labels, values, color=['blue', 'red'], alpha=0.7)
axs[1, 1].set_yscale('log') # Skala logarytmiczna z uwagi na gigantyczną różnicę
axs[1, 1].set_title("Całkowita liczba wywołań (Skala logarytmiczna)")
axs[1, 1].set_ylabel("Liczba wywołań (log)")

# Dodanie wartości nad słupkami
for bar in bars:
    yval = bar.get_height()
    axs[1, 1].text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center', fontsize=10)

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Marginesy na tytuł główny

# Zapis do pliku
plik_wykresu = "wykresy_dokumentacja.png"
plt.savefig(plik_wykresu, dpi=300)
print(f"✅ Zapisano panel z wykresami jako: {plik_wykresu}")
plt.show()