# BinanceTraderBot


Zaawansowany bot handlujący na giełdzie Binance napisany w C# i Pythonie.
C# obsługuje sygnały z TradingView, automatycznie generuje zlecenia z wbudowanej
strategii RSI oraz zarządza stop-lossem i take-profitem. Moduł Python służy do
optymalizacji parametrów strategii oraz porównywania kilku podejść (RSI, MACD).

Najnowsza wersja skanuje pary z największym wolumenem, a strategia w C# bierze
pod uwagę wzrost aktywności wolumenowej. W katalogu `ml_optimizer` znajdują się
skrypty do trenowania prostego modelu RL (`rl_optimizer.py`) oraz testu kilku
strategii (`compare_strategies.py`).


## Wymagania
- .NET 6 SDK
- Python 3.8+

## Instalacja
1. Zainstaluj wymagane biblioteki Pythona:
   ```bash
   pip install -r TradingBotTV/ml_optimizer/requirements.txt
   ```
2. Zbuduj projekt C#:
   ```bash
   dotnet build TradingBotTV/bot/BinanceTraderBot.csproj
   ```

## Uruchomienie
1. Uzupełnij klucze API w pliku `TradingBotTV/config/settings.json`.
2. W katalogu `TradingBotTV/bot` uruchom aplikację:
   ```bash
   dotnet run --project BinanceTraderBot.csproj
   ```


W pliku `config/settings.json` możesz ustawić dodatkowo poziom `stopLossPercent`
i `takeProfitPercent`, które określają dystans w procentach od ceny wejścia.

Bot nasłuchuje na `http://localhost:5000/webhook` i co godzinę uruchamia proces samouczenia strategii. Moduł `auto_optimizer.py` losuje nowe progi RSI na podstawie dotychczasowych wyników i zapisuje najlepsze parametry w pliku `model_state.json`. Zaktualizowane wartości są automatycznie wczytywane do konfiguracji.
`StrategyEngine` co minutę pobiera bieżące notowania i samodzielnie składa zlecenia. Wysoki wolumen zwiększa szansę na wygenerowanie sygnału.

Proces optymalizacji (`auto_optimizer.py` lub `rl_optimizer.py`) uruchamia się raz na godzinę i zapisuje najlepsze parametry w `model_state.json`.

### Narzędzia ML
* `auto_optimizer.py` – losowe poszukiwanie progów RSI
* `rl_optimizer.py` – prosty przykład uczenia ze wzmocnieniem
* `compare_strategies.py` – backtest RSI vs. MACD

Aby uruchomić test porównawczy strategii:
```bash
python TradingBotTV/ml_optimizer/compare_strategies.py BTCUSDT
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
