# Struktura projektu BinanceTraderBot

Poniżej znajduje się opis plików i katalogów w repozytorium. Wszystkie nazwy plików zostały zachowane w oryginalnej formie, a komentarze w języku polskim wyjaśniają do czego służą.

## Główne katalogi

- **TradingBotTV/bot** – kod bota w C#. Obsługuje sygnały z TradingView, wykonuje zlecenia i uruchamia optymalizację ML.
- **TradingBotTV/config** – plik `settings.json` z kluczami API i parametrami strategii.
- **TradingBotTV/ml_optimizer** – moduły Pythona do backtestów i optymalizacji.
- **docs** – dodatkowa dokumentacja (np. ten plik, `repo_analysis.md`).

## Ważne pliki

### C#
- `Program.cs` – punkt wejścia aplikacji; uruchamia serwer webhook i silnik strategii.
- `WebhookServer.cs` – prosty serwer HTTP nasłuchujący na `/webhook`.
- `StrategyEngine.cs` – implementacja strategii RSI i logiki wolumenu.
- `BinanceTrader.cs` – wysyłanie zleceń do Binance.
- `ConfigManager.cs` – wczytywanie i aktualizowanie konfiguracji.
- `OptimizerRunner.cs` – wywołanie optymalizatorów Pythona z poziomu C#.
- `SymbolScanner.cs` – wyszukiwanie najpopularniejszych par handlowych.

### Python (`ml_optimizer`)
- `data_fetcher.py` – pobieranie świec z Binance i zapisywanie ich w `ml_optimizer/data` (cache dla pracy offline).
- `backtest.py` – funkcje do obliczania RSI/MACD oraz prosty backtest strategii.
- `auto_optimizer.py` – losowe poszukiwanie najlepszych progów RSI; wyniki zapisywane są w `model_state.json`.
- `optimizer.py` – przykład prostej optymalizacji parametrów w pętli.
- `compare_strategies.py` – porównanie wyników strategii RSI i MACD.
- `rl_optimizer.py` – uproszczony przykład uczenia ze wzmocnieniem.
- `tests/test_backtest.py` – testy jednostkowe dla modułu `backtest.py`.

## Edycja ustawień

Najważniejsze parametry znajdują się w pliku `TradingBotTV/config/settings.json`:

```json
{
  "binance": {
    "apiKey": "TWOJ_API_KEY",
    "apiSecret": "TWOJ_SECRET_KEY"
  },
  "trading": {
    "symbol": "BTCUSDT",
    "amount": 0.001,
    "rsiBuyThreshold": 30,
    "rsiSellThreshold": 70,
    "stopLossPercent": 1.5,
    "takeProfitPercent": 3.0
  }
}
```

- `symbol` – domyślna para handlowa.
- `amount` – ilość kupowana/sprzedawana w pojedynczej transakcji.
- `rsiBuyThreshold` i `rsiSellThreshold` – progi RSI wykorzystywane w strategii.
- `stopLossPercent` i `takeProfitPercent` – ustawienia SL/TP w procentach.

Optymalizatory Pythona mogą modyfikować te wartości automatycznie (zapis w `model_state.json` i aktualizacja przez `OptimizerRunner`).

## Jak uruchomić testy

1. Zainstaluj zależności Pythona: `pip install -r TradingBotTV/ml_optimizer/requirements.txt`
2. Uruchom testy: `pytest`

Pliki w C# wymagają .NET 6. Informacje o budowaniu i uruchamianiu znajdują się w głównym pliku `README.md`.

