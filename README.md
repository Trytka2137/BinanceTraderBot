# BinanceTraderBot

 5x627e-codex/sprawdź-poprawność-kodu
Zaawansowany bot handlujący na giełdzie Binance napisany w C# i Pythonie. 
C# obsługuje sygnały z TradingView, automatycznie generuje zlecenia z wbudowanej
strategii RSI oraz zarządza stop-lossem i take-profitem. Moduł Python służy do
optymalizacji parametrów strategii.
Prosty bot handlujący na giełdzie Binance napisany w C# i Pythonie. Część C# obsługuje sygnały webhook i wykonuje transakcje, a moduł Python służy do optymalizacji parametrów strategii RSI.
BOT

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

''<<<<<<< 5x627e-codex/sprawdź-poprawność-kodu
W pliku `config/settings.json` możesz ustawić dodatkowo poziom `stopLossPercent`
i `takeProfitPercent`, które określają dystans w procentach od ceny wejścia.

Bot nasłuchuje na `http://localhost:5000/webhook` i co godzinę uruchamia proces samouczenia strategii. Moduł `auto_optimizer.py` losuje nowe progi RSI na podstawie dotychczasowych wyników i zapisuje najlepsze parametry w pliku `model_state.json`. Zaktualizowane wartości są automatycznie wczytywane do konfiguracji.
`StrategyEngine` co minutę pobiera bieżące notowania i samodzielnie składa zlecenia na podstawie RSI.

=======
 5xz69j-codex/sprawdź-poprawność-kodu
Bot nasłuchuje na `http://localhost:5000/webhook` i co godzinę uruchamia proces samouczenia strategii. Moduł `auto_optimizer.py` losuje nowe progi RSI na podstawie dotychczasowych wyników i zapisuje najlepsze parametry w pliku `model_state.json`. Zaktualizowane wartości są automatycznie wczytywane do konfiguracji.


Bot nasłuchuje na `http://localhost:5000/webhook` i co godzinę uruchamia proces optymalizacji parametrów strategii.

hm8wp8-codex/sprawdź-poprawność-kodu
BOT
BOT
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

 5x627e-codex/sprawdź-poprawność-kodu

5xz69j-codex/sprawdź-poprawność-kodu

BOT

BOT
Komunikaty o błędach połączeń z API są wypisywane w konsoli, dzięki czemu łatwiej zdiagnozować problemy sieciowe.

> **Uwaga:** W środowiskach bez dostępu do API Binance wykonywanie zapytań do `api.binance.com` może zakończyć się błędem.
