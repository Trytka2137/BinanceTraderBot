# BinanceTraderBot

Prosty bot handlujący na giełdzie Binance napisany w C# i Pythonie. Część C# obsługuje sygnały webhook i wykonuje transakcje, a moduł Python służy do optymalizacji parametrów strategii RSI.

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

Bot nasłuchuje na `http://localhost:5000/webhook` i co godzinę uruchamia proces optymalizacji parametrów strategii.

> **Uwaga:** W środowiskach bez dostępu do API Binance wykonywanie zapytań do `api.binance.com` może zakończyć się błędem.
