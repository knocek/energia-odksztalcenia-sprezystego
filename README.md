# Energia odkształcenia sprężystego: objętościowa i postaciowa

Program służy do obliczania gęstości energii odkształcenia sprężystego w punkcie materiału izotropowego. Na podstawie podanego tensora odkształceń oraz parametrów materiałowych program wyznacza część objętościową i postaciową energii sprężystej.

## Cel programu

Celem programu jest:

- wczytanie tensora odkształceń `ε` w postaci macierzy 3×3,
- wczytanie parametrów materiałowych: modułu Younga `E` oraz współczynnika Poissona `ν`,
- obliczenie odkształcenia średniego,
- obliczenie modułu ściśliwości objętościowej `K` oraz modułu Kirchhoffa `μ`,
- wyznaczenie tensora dewiatorowego odkształceń,
- obliczenie energii objętościowej, postaciowej i całkowitej,
- obliczenie naprężenia średniego,
- wygenerowanie wykresu zależności energii objętościowej i postaciowej od odkształcenia średniego.

## Wykorzystane biblioteki

Biblioteka `numpy` jest używana do wykonywania obliczeń macierzowych, takich jak zapis tensora odkształceń, obliczenie śladu macierzy oraz tensora dewiatorowego.

Biblioteka `matplotlib` służy do wykonania wykresu zależności energii objętościowej i postaciowej od odkształcenia średniego.

Biblioteka `tkinter` została wykorzystana do utworzenia prostego interfejsu graficznego, który umożliwia wprowadzenie danych, uruchomienie obliczeń, wyświetlenie wyników oraz zapisanie wykresu.

Dodatkowo wykorzystano moduł `math` do formatowania wyników w notacji naukowej.

## Podstawy teoretyczne

W programie wykorzystano następujące zależności:

- Odkształcenie średnie:
εm = (εxx + εyy + εzz) / 3

- Moduł objętościowy:
K = E / [3(1 - 2ν)]

- Moduł Kirchhoffa:
μ = E / [2(1 + ν)]

- Tensor dewiatorowy:
ε' = ε − εm I

- Energia objętościowa:
Φv = 1/2 · K · (3εm)²

- Energia postaciowa:
Φs = μ Σ ε'ij²

- Naprężenie średnie:
σm = 3Kεm

## Dane wejściowe

Użytkownik podaje:

- tensor odkształceń ε jako macierz 3×3,
- moduł Younga E,
- współczynnik Poissona ν.

Przykładowy tensor odkształceń ma postać:

`[0.001, 0.0002, 0.0000],`
`[0.0002, 0.0005, 0.0001],`
`[0.0000, 0.0001, -0.0003]`

Przykładowy mnożnik tensora: `10^-4`
Przykładowy moduł Younga: `210e9`
Przykładowy współczynnik Poissona: `0,3`

### Format danych wejściowych

Program obsługuje różne formaty zapisu liczb:

- zapis dziesiętny: 0.001
- zapis wykładniczy: 1e-3
- zapis inżynierski: 10^-3 lub 3*10^-4

Możliwe jest również zastosowanie wspólnego mnożnika dla całego tensora.

## Wyniki programu

Program wyświetla:

- odkształcenie średnie εm,
- moduł objętościowy K,
- moduł Kirchoffa μ,
- naprężenie średnie σm,
- tensor dewiatorowy odkształceń ε',
- energię objętościową Φv,
- energię postaciową Φs,
- energię całkowitą Φ,
- wykres zależności Φv(εm) i Φs(εm).

## Interpretacja wykresu

Wykres przedstawia zależność energii od odkształcenia średniego εm przy stałym tensorze dewiatorowym.

- Energia objętościowa Φv zmienia się wraz z εm (parabola),
- Energia postaciowa Φs pozostaje stała, ponieważ tensor dewiatorowy ε' nie zmienia się podczas analizy.

W szczególnych przypadkach:

- dla czystej zmiany objętości Φs = 0,
- dla czystej zmiany kształtu Φv = 0.

## Sposób działania programu

Program najpierw pobiera dane wejściowe od użytkownika. Następnie oblicza podstawowe parametry materiałowe oraz rozkłada tensor odkształceń na część średnią i dewiatorową. Na tej podstawie wyznaczana jest energia sprężysta związana ze zmianą objętości oraz energia związana ze zmianą postaci.

Program generuje wykres zależności Φv i Φs od εm oraz umożliwia jego zapis do pliku.

## Kontrola poprawności danych

Program sprawdza, czy podany tensor odkształceń jest symetryczny. Z fizycznego punktu widzenia tensor małych odkształceń powinien spełniać warunek:

εij = εji

Oznacza to, że:

- εxy = εyx,
- εxz = εzx,
- εyz = εzy.

Jeżeli tensor nie jest symetryczny, program wyświetla ostrzeżenie oraz informuje, które składowe są niezgodne. Użytkownik może przerwać obliczenia albo kontynuować, mając świadomość, że wynik nie ma poprawnej interpretacji fizycznej.

## 📁 Struktura projektu

energia_odksztalcenia/
│
├── main.py              # punkt startowy programu - tryb CLI/GUI
├── calculations.py      # wzory i obliczenia
├── cli.py               # wersja konsolowa
├── gui.py               # interfejs graficzny (Tkinter)
├── interpretation.py    # interpretacja wyników
├── plot.py              # generowanie wykresów
│
├── requirements.txt     # wymagane biblioteki
└── README.md

`tkinter` jest częścią standardowej instalacji Pythona, dlatego nie znajduje się w pliku `requirements.txt`.

## Tryby pracy

Program może działać w dwóch trybach:

- GUI (interfejs graficzny – tkinter)
- CLI (tryb tekstowy)

Jeżeli tkinter nie jest dostępny, program automatycznie przechodzi do trybu CLI.

## Uruchomienie programu

Aby uruchomić program, należy zainstalować wymagane biblioteki:

```bash
python -m venv venv # stworzenie wirtualnego środowiska
venv\Scripts\activate # aktywacja środowiska
pip install -r requirements.txt # zainstalowanie zależności
python main.py # uruchomienie programu
```

## Interpretacja wyników

Energia objętościowa opisuje część energii sprężystej związaną ze zmianą objętości materiału. Zależy ona od odkształcenia średniego oraz modułu ściśliwości objętościowej.

Energia postaciowa opisuje część energii sprężystej związaną ze zmianą kształtu materiału bez zmiany jego objętości. Jest ona zależna od tensora dewiatorowego odkształceń oraz modułu Kirchhoffa.

Energia całkowita jest sumą energii objętościowej i postaciowej:
Φ = Φv + Φs

Wykres pozwala porównać wpływ odkształcenia średniego na energię objętościową i postaciową.
