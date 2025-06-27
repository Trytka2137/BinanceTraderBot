# BinanceTraderBot

Zaawansowany bot handlujący na giełdzie Binance napisany w C# i Pythonie.
C# obsługuje sygnały z TradingView, automatycznie generuje zlecenia z wbudowanej
strategii RSI oraz zarządza stop-lossem i take-profitem. Moduł Python służy do
optymalizacji parametrów strategii oraz porównywania kilku podejść (RSI, MACD).

Najnowsza wersja skanuje pary z największym wolumenem, a strategia w C# bierze
pod uwagę wzrost aktywności wolumenowej. Dodano obsługę trailing stop oraz
dynamiczne dostosowanie wielkości pozycji w zależności od zmienności rynku.
Bot samoczynnie wyłącza handel, gdy łączna strata przekroczy ustawiony próg `maxDrawdownPercent`.

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
3. Zbuduj projekt C#:
   ```bash
   dotnet build TradingBotTV/bot/BinanceTraderBot.csproj
   ```

## Uruchomienie
1. Uzupełnij klucze API w pliku `TradingBotTV/config/settings.json` lub ustaw
   zmienne środowiskowe `BINANCE_API_KEY` i `BINANCE_API_SECRET`. Możesz też
   utworzyć plik `.env` z tymi wartościami, a bot wczyta je automatycznie.
2. W katalogu `TradingBotTV/bot` uruchom aplikację:
   ```bash
   dotnet run --project BinanceTraderBot.csproj
   ```



W pliku `config/settings.json` możesz ustawić dodatkowo poziom `stopLossPercent` i `takeProfitPercent`, a także `maxDrawdownPercent`, który określa poziom straty (w % od kapitału początkowego) po przekroczeniu którego handel zostanie automatycznie wyłączony. Można też zmienić okresy `emaShortPeriod` i `emaLongPeriod` wykorzystywane w filtrze trendu.

### Parametry konfiguracyjne

Szczegółowy opis wszystkich pól znajduje się w [docs/README_pl.md](docs/README_pl.md).

Bot nasłuchuje na `http://localhost:5000/webhook` i uruchamia proces samouczenia strategii co 15, 30 oraz 60 minut. Moduł `auto_optimizer.py` losuje nowe progi RSI na podstawie dotychczasowych wyników i zapisuje najlepsze parametry w pliku `model_state.json`. Zaktualizowane wartości są automatycznie wczytywane do konfiguracji.
`StrategyEngine` co minutę pobiera bieżące notowania i samodzielnie składa zlecenia. Wysoki wolumen zwiększa szansę na wygenerowanie sygnału.
Bot nawiązuje także stałe połączenie WebSocket z Binance, a opcjonalnie z TradingView, jeśli podasz adres w konfiguracji.

Uruchomiono również panel na `http://localhost:5001`, który pozwala podejrzeć logi,
wynik PnL i w razie potrzeby włączyć lub zatrzymać handel.

Proces optymalizacji (`auto_optimizer.py` lub `rl_optimizer.py`) wykonuje się automatycznie co 15, 30 i 60 minut, zapisując najlepsze parametry w `model_state.json`.

Źródłem danych do uczenia jest Binance. Moduł `data_fetcher.py` pobiera historyczne
dane świecowe z API giełdy i zapisuje je w katalogu `ml_optimizer/data`. Przy
braku połączenia z siecią wykorzystywana jest ostatnia zapisana kopia, dzięki
czemu optymalizacja może przebiegać również offline.

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
* `tradingview_auto_trader.py` – pobiera rekomendacje z TradingView i wysyła
  sygnały do lokalnego webhooka. Funkcja `async_auto_trade_from_tv` pozwala
  obsłużyć wiele symboli równolegle.

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

1. Zainstaluj zależności Pythona:
   ```bash
   pip install -r TradingBotTV/ml_optimizer/requirements.txt
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

Więcej informacji znajdziesz w pliku [docs/README_pl.md](docs/README_pl.md).
