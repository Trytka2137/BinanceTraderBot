# BinanceTraderBot

Zaawansowany bot handlujący na giełdzie Binance napisany w C# i Pythonie.
C# obsługuje sygnały z TradingView, automatycznie generuje zlecenia z wbudowanej
strategii RSI oraz zarządza stop-lossem i take-profitem. Moduł Python służy do
optymalizacji parametrów strategii oraz porównywania kilku podejść (RSI, MACD).

Najnowsza wersja skanuje pary z największym wolumenem, a strategia w C# bierze
pod uwagę wzrost aktywności wolumenowej. Dodano obsługę trailing stop oraz
dynamiczne dostosowanie wielkości pozycji w zależności od zmienności rynku.
Bot samoczynnie wyłącza handel, gdy łączna strata przekroczy ustawiony próg `maxDrawdownPercent`.

W folderze `ml_optimizer` pojawiły się moduły `risk`, `analytics` i `sentiment`,
które umożliwiają obliczanie Kelly Criterion, Value at Risk, Bollinger Bands,
oscylatora stochastycznego oraz prostą ocenę nastrojów inwestorów. Dodano
również moduł `fundamental` z funkcjami pobierającymi dane z CoinMarketCap,
CoinGecko, Messari i GitHuba. Moduł `sentiment` potrafi teraz pobrać wartość
Crypto Fear & Greed Index i wskaźnik nastrojów z LunarCrush.
Dodano też moduł `ml_models` z prostymi modelami predykcyjnymi oraz funkcję
`backtest_tick_strategy` pozwalającą testować strategie na danych sekundowych
z uwzględnieniem poślizgu i prowizji.
Pojawiły się moduły `portfolio`, `orderbook`, `hedging` i `arbitrage`, które
ułatwiają zarządzanie wieloma symbolami, analizę księgi zleceń w czasie
rzeczywistym oraz zabezpieczanie pozycji kontraktami futures lub wyszukiwanie
okazji arbitrażowych.

Repozytorium zawiera także moduły `execution` (TWAP, VWAP), `hft` z prostymi
sygnałami z orderbooka oraz `options` wykorzystujący model Black-Scholes i
strategię straddle. W `ml_models` dostępna jest funkcja `train_deep_learning_model`.

Strategia łączy sygnały z interwałów 1m, 30m i 1h, filtruje trend na podstawie średnich EMA (50 i 200) i zapisuje logi do pliku `logs/bot.log`. Moduł `ml_optimizer` zawiera skrypty do optymalizacji parametrów i trenowania modelu RL (`rl_optimizer.py`) oraz porównywania strategii (`compare_strategies.py`).

Najświeższe skrypty Pythona wykorzystują własny plik logów `TradingBotTV/ml_optimizer/state/ml_optimizer.log` (rotacja plików) oraz prosty moduł monitoringu zapisujący statystyki w `TradingBotTV/ml_optimizer/state/metrics.csv`. Operacje sieciowe (pobieranie danych, wysyłanie webhooków, klonowanie repozytoriów) są teraz powtarzane kilkukrotnie z rosnącym opóźnieniem, co zwiększa odporność na chwilowe problemy z siecią.




## Wymagania
- .NET 8 SDK
- Python 3.8+

## Instalacja
1. Zainstaluj pakiet `.NET 8 SDK`:
   - **Ubuntu**
     ```bash
     sudo apt-get update
     sudo apt-get install -y dotnet-sdk-8.0
     ```
   - **Windows** – pobierz instalator z [dotnet.microsoft.com](https://dotnet.microsoft.com/download/dotnet/8.0)
     i uruchom lub skorzystaj z `winget`:
     ```powershell
     winget install Microsoft.DotNet.SDK.8
     ```
2. Zainstaluj wymagane biblioteki Pythona:
   ```bash
   pip install -r TradingBotTV/ml_optimizer/requirements.txt
   # lub zainstaluj cały moduł
   pip install .
   ```
   Jeśli instalacja zakończy się błędem z powodu zablokowanego dostępu do
   `pypi.org` lub `files.pythonhosted.org`, ustaw zmienne środowiskowe proxy albo
   zainstaluj pakiety z wcześniej pobranych plików `.whl`. Możesz sprawdzić
   łączność poleceniem:
   ```bash
   python -m TradingBotTV.ml_optimizer.network_utils https://pypi.org
   ```
3. Zbuduj projekt C#:
   ```bash
   dotnet build TradingBotTV/bot/BinanceTraderBot.csproj
   ```

## Konfiguracja
1. Uzupełnij klucze API w pliku `TradingBotTV/config/settings.json` lub ustaw
   zmienne środowiskowe `BINANCE_API_KEY` i `BINANCE_API_SECRET`. Możesz też
   utworzyć plik `.env` z tymi wartościami.
2. W tym samym pliku możesz zmienić takie parametry jak `stopLossPercent`,
   `takeProfitPercent`, `trailingStopPercent`, `maxDrawdownPercent` oraz okresy
   EMA.

## Uruchomienie
1. W katalogu `TradingBotTV/bot` uruchom aplikację:
   ```bash
   dotnet run --project BinanceTraderBot.csproj
   ```




### Parametry konfiguracyjne

Szczegółowy opis wszystkich pól znajduje się w [docs/README_pl.md](docs/README_pl.md).

Bot nasłuchuje na `http://localhost:5000/webhook` i uruchamia proces samouczenia strategii co 15, 30 oraz 60 minut. Moduł `auto_optimizer.py` losuje nowe progi RSI na podstawie dotychczasowych wyników i zapisuje najlepsze parametry w pliku `model_state.json`. Zaktualizowane wartości są automatycznie wczytywane do konfiguracji.
`StrategyEngine` co minutę pobiera bieżące notowania i samodzielnie składa zlecenia. Wysoki wolumen zwiększa szansę na wygenerowanie sygnału.
Bot nawiązuje także stałe połączenie WebSocket z Binance, a opcjonalnie z TradingView, jeśli podasz adres w konfiguracji.

Uruchomiono również panel na `http://localhost:5001`, który pozwala podejrzeć logi,
wynik PnL i w razie potrzeby włączyć lub zatrzymać handel.

Proces optymalizacji (`auto_optimizer.py` lub `rl_optimizer.py`) wykonuje się automatycznie co 15, 30 i 60 minut, zapisując najlepsze parametry w `model_state.json`.

Źródłem danych do uczenia jest Binance. Moduł `data_fetcher.py` pobiera świeże
dane OHLCV przez Binance API, a starsze notowania pobiera z CoinGecko.
Zarówno klines z Binance, jak i wyniki zapytań do CoinGecko są buforowane w
`ml_optimizer/data`, dzięki czemu optymalizacja może przebiegać offline przy
braku połączenia z siecią.
Dane są zapisywane w katalogu `ml_optimizer/data`, dzięki czemu optymalizacja
może przebiegać również offline przy braku połączenia z siecią.


### Monitoring i logi
Logi modułów Pythona zapisywane są w `TradingBotTV/ml_optimizer/state/ml_optimizer.log`. W pliku `TradingBotTV/ml_optimizer/state/metrics.csv` gromadzone są podstawowe metryki, takie jak najlepsze uzyskane PnL. Zaimplementowano ponawianie zapytań sieciowych, dlatego pobieranie danych i wysyłanie sygnałów jest odporniejsze na przejściowe problemy z siecią.

### Sprawdzanie dostępu do API
Skrypt `network_utils.py` umożliwia szybkie zweryfikowanie, czy Twoje środowisko
ma połączenie z oficjalnymi adresami (np. `https://api.binance.com`).
Przykład użycia:

```bash
python -m TradingBotTV.ml_optimizer.network_utils https://api.binance.com
```
Funkcja `check_connectivity` zwróci `True`, jeśli serwis odpowie, inaczej `False`.
Możesz skorzystać także z `async_check_connectivity`, by wykonywać test
w środowiskach asynchronicznych.

### Narzędzia ML
* `auto_optimizer.py` – losowe poszukiwanie progów RSI
* `rl_optimizer.py` – prosty przykład uczenia ze wzmocnieniem
* `compare_strategies.py` – backtest RSI vs. MACD
* `github_strategy_simulator.py` – klonuje repozytoria z GitHub i symuluje
  zdefiniowane w nich strategie offline
* `ml_models.py` – proste modele predykcyjne (RandomForest) i optymalizacja
  hiperparametrów
* `backtest_tick_strategy` – testy na danych 1‑sekundowych z uwzględnieniem
  opóźnień i kosztów transakcyjnych
* `portfolio.py` – zarządzanie wieloma instrumentami jednocześnie
* `orderbook.py` – obliczanie best bid/ask i wskaźnika przepływu zleceń
* `hedging.py` – szacowanie wielkości pozycji zabezpieczającej
* `arbitrage.py` – sprawdzanie różnic cen między giełdami
* `execution.py` – algorytmy TWAP i VWAP
* `hft.py` – proste sygnały z mikrostruktury rynku
* `options.py` – wycena opcji Black-Scholes i strategia straddle

Aby uruchomić test porównawczy strategii:
```bash
python TradingBotTV/ml_optimizer/compare_strategies.py BTCUSDT
```

### Testy
W katalogu projektu uruchom testy poleceniem:
```bash
pytest
```
Przed wysłaniem zmian uruchom również `flake8`, aby upewnić się, że kod spełnia
standard PEP8:
```bash
flake8
```


### Sygnały z TradingView
W alertach TradingView ustaw adres webhook na `http://localhost:5000/webhook`.
Przykładowa treść powiadomienia:

```json
{
  "ticker": "BTCUSDT",
  "strategy": { "order_action": "buy" }
}
```
Pole `order_action` może przyjmować wartości `buy` lub `sell`.


Komunikaty o błędach połączeń z API są wypisywane w konsoli, dzięki czemu łatwiej zdiagnozować problemy sieciowe.

> **Uwaga:** W środowiskach bez dostępu do API Binance wykonywanie zapytań do `api.binance.com` może zakończyć się błędem.

## Licencja

Projekt jest dostępny na licencji MIT. Szczegóły znajdziesz w pliku [LICENSE](LICENSE).

## Wkład w rozwój

Przed wysłaniem zmian:

1. Zainstaluj zależności Pythona i `flake8`:
   ```bash
   pip install -r TradingBotTV/ml_optimizer/requirements.txt
   pip install flake8
   ```
2. Upewnij się, że wszystkie testy przechodzą:
   ```bash
   pytest
   ```
3. Sprawdź styl kodu:
   ```bash
   flake8
   ```
4. W opisie PR napisz skrótowy opis zmian i dodaj informację, czy testy zakończyły się sukcesem.

Zobacz także plik [TODO.md](TODO.md) zawierający listę planowanych usprawnień.

### Źródła analizy fundamentalnej i sentymentu

- CoinMarketCap, CoinGecko – ogólne dane rynkowe
- Messari, Token Terminal – raporty i przychody projektów
- GitHub – statystyki aktywności deweloperów
- Certik, Quantstamp – status audytów smart kontraktów
- Glassnode, CryptoQuant, Santiment – wskaźniki on‑chain i sentyment
- Etherscan, Solscan – eksploratory blockchaina
- Crypto Fear & Greed Index, LunarCrush – gotowe wskaźniki nastroju

Więcej informacji znajdziesz w pliku [docs/README_pl.md](docs/README_pl.md).
