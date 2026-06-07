```wl
In[]:= 
  (* ====================SYSTEM OPCJI I PRZEŁĄCZNIKÓW====================*)(*WYBÓR KIERUNKU:wpisz OdPoczatku lub OdKonca*) 
   wybranyKierunek = "OdPoczatku"; 
    
   (* ====================KONFIGURACJA WEJŚCIOWA====================*) 
    wybranyAlfabet = {"a", "b", "c"}; 
    liczbaIteracji = 120; (*Ile kolejnych słów wygenerować (razem będzie 1+liczbaIteracji) o ile nie zostanie wcześniej przerwane*) 
    
   (* ====================DEFINICJA METODY WERYFIKACJI====================*) 
    
   (*Weryfikacja oparta na wzorcach tekstowych*) 
    SprawdzajBezkwadratowoscQ[tekst_] := StringFreeQ[tekst, x__ ~~ x__]; 
    
    
   (* ====================AKTYWNE FUNKCJE SZUKAJĄCE====================*) 
    
    ZnajdzRozszerzenieSlowaOdPoczatku[aktualneSlowo_String, alfabet_List] := Catch[Block[{potencjalneSlowo}, Do[If[SprawdzajBezkwadratowoscQ[potencjalneSlowo = StringInsert[aktualneSlowo, litera, pozycja]], Throw[{potencjalneSlowo, pozycja}]], {pozycja, 1, StringLength[aktualneSlowo] + 1}, {litera, alfabet}]; 
        $Failed]]; 
    
    ZnajdzRozszerzenieSlowaOdKonca[aktualneSlowo_String, alfabet_List] := Catch[Block[{potencjalneSlowo}, Do[If[SprawdzajBezkwadratowoscQ[potencjalneSlowo = StringInsert[aktualneSlowo, litera, -pozycjaOdKonca]], Throw[{potencjalneSlowo, -pozycjaOdKonca}]], {pozycjaOdKonca, StringLength[aktualneSlowo] + 1}, {litera, alfabet}]; 
        $Failed (*Zwraca $Failed,gdy pętla przejdzie całe słowo bez sukcesu*)]]; 
    
   (*Dynamiczne podstawienie wybranej funkcji na żądanie użytkownika*) 
    WykonajRozszerzenie[slowo_, alf_] := If[wybranyKierunek === "OdPoczatku", ZnajdzRozszerzenieSlowaOdPoczatku[slowo, alf], ZnajdzRozszerzenieSlowaOdKonca[slowo, alf]]; 
    
    
   (* ====================GENEROWANIE DANYCH====================*) 
    
    pierwszeSlowoStartowe = wybranyAlfabet[[1]]; 
    powodZakonczenia = "Osiagnieto limit iteracji"; 
    
    czasIwynikiAlgorytmu = AbsoluteTiming[Block[{biezaceSlowo = pierwszeSlowoStartowe, tabelaDanychCSV, rezultatRozszerzenia, dlugoscBiezacegoSlowa, indeksWstawieniaLitery, numerKroku = 1}, tabelaDanychCSV = {{"DlugoscSlowa", "SlowoBezKwadratow", "ParametrPrzesuniecia"}}; 
        If[wybranyKierunek === "OdPoczatku", AppendTo[tabelaDanychCSV, {StringLength[biezaceSlowo], biezaceSlowo, 1}],AppendTo[tabelaDanychCSV, {StringLength[biezaceSlowo], biezaceSlowo, -1}]]; 
        
        While[numerKroku <= liczbaIteracji, rezultatRozszerzenia = WykonajRozszerzenie[biezaceSlowo, wybranyAlfabet]; 
         If[rezultatRozszerzenia === $Failed, powodZakonczenia = "Algorytm utknal - brak mozliwosci dalszego rozszerzenia slowa"; 
          Print[powodZakonczenia, " na kroku ", numerKroku]; 
          Break[];]; 
         biezaceSlowo = rezultatRozszerzenia[[1]]; 
         indeksWstawieniaLitery = rezultatRozszerzenia[[2]]; 
         dlugoscBiezacegoSlowa = StringLength[biezaceSlowo]; 
         AppendTo[tabelaDanychCSV, {dlugoscBiezacegoSlowa, biezaceSlowo, indeksWstawieniaLitery}]; 
         numerKroku++;]; 
        tabelaDanychCSV]]; 
    
    
   (* ====================PRZYGOTOWANIE WYNIKÓW i ZAPIS====================*) 
    
    calkowityCzasSekundy = czasIwynikiAlgorytmu[[1]]; 
    finalnaTabelaWynikow = czasIwynikiAlgorytmu[[2]]; 
    
    Print["Zakończono! Kierunek: ", wybranyKierunek]; 
    Print["Czas wykonania: ", calkowityCzasSekundy, " sekund. Powód: ",powodZakonczenia]; 
    
    znacznikCzasu = DateString[{"Year", "-", "Month", "-", "Day", "_", "Hour", "-", "Minute"}]; 
    nazwaPlikuCSV = StringJoin[znacznikCzasu, "_", "wynik_algorytmu_", wybranyKierunek, ".csv"]; 
    
    tabelaDoZapisu = finalnaTabelaWynikow; 
    Do[tabelaDoZapisu[[i, 2]] = "\"" <> ToString[tabelaDoZapisu[[i, 2]]] <> "\"", {i, 2, Length[tabelaDoZapisu]}]; 
    
    AppendTo[tabelaDoZapisu, {"", "", ""}]; 
    AppendTo[tabelaDoZapisu, {"Status zakonczenia:", powodZakonczenia, ""}]; 
    AppendTo[tabelaDoZapisu, {"Kierunek szukania:", wybranyKierunek, ""}]; 
    AppendTo[tabelaDoZapisu, {"Czas wykonania (s):", calkowityCzasSekundy, ""}]; 
    
    Export[FileNameJoin[{NotebookDirectory[], nazwaPlikuCSV}], Prepend[tabelaDoZapisu, {"sep=,"}], "CSV", "ItemSeparators" -> ",","TextDelimiters" -> "\""]; 
   
```

![0xz0177h8qkg4](img/0xz0177h8qkg4.png)

![17snliwq4gbt3](img/17snliwq4gbt3.png)