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
- `data_fetcher.py` – pobieranie świec z Binance i CoinGecko oraz zapisywanie ich w `ml_optimizer/data` (cache dla pracy offline).
- `backtest.py` – funkcje do obliczania RSI/MACD oraz prosty backtest strategii.
- `auto_optimizer.py` – losowe poszukiwanie najlepszych progów RSI; wyniki zapisywane są w `model_state.json`.
- `optimizer.py` – przykład prostej optymalizacji parametrów w pętli.
- `compare_strategies.py` – porównanie wyników strategii RSI i MACD.
- `auto_select_best_strategy` w `compare_strategies.py` – automatyczny wybór najlepszej techniki (walidacja czasowa).
- `should_switch_strategy` w `compare_strategies.py` – podejmuje decyzję o zmianie strategii.
- `detect_price_anomalies` w `analytics.py` – wskazuje anomalie cenowe.
- `online_q_learning` w `deep_rl_examples.py` – uczy model na strumieniu danych.
- `rl_optimizer.py` – rozbudowany przykład uczenia ze wzmocnieniem.
- `optuna_optimize` w `auto_ml.py` – tuning parametrów z wykorzystaniem Optuna.
- `fetch_social_media_sentiment` w `sentiment.py` – analiza mediów społecznościowych.
- `autoencoder_anomaly_scores` w `analytics.py` – wykrywanie anomalii autoenkoderem.
- `github_strategy_simulator.py` – pobieranie strategii z publicznych repozytoriów
  i ich symulacja offline.
- `portfolio.py` – alokacja kapitału na wiele par jednocześnie
- `orderbook.py` – analiza order book i obliczanie best bid/ask
- `hedging.py` – obliczanie wielkości pozycji zabezpieczającej
- `arbitrage.py` – prosty kalkulator różnic cen
- `logger.py` – wspólne funkcje logujące zapisujące zdarzenia w `state/ml_optimizer.log`.
- `monitor.py` – prosty rejestrator metryk tworzący plik `state/metrics.csv`.
- `network_utils.py` – sprawdzanie dostępu do wybranych adresów URL (funkcje
  `check_connectivity` i `async_check_connectivity`).
  i wysyłanie sygnałów do lokalnego webhooka.
- `logger.py` – wspólne funkcje logujące zapisujące zdarzenia w `state/ml_optimizer.log`.
- `monitor.py` – prosty rejestrator metryk tworzący plik `state/metrics.csv`.
- `network_utils.py` – sprawdzanie dostępu do wybranych adresów URL.
- `tests/test_backtest.py` – testy jednostkowe dla modułu `backtest.py`.

## Instalacja i konfiguracja

1. Zainstaluj Python 3.8+ oraz .NET 8 SDK.
2. Zainstaluj zależności:
   ```bash
   pip install -r TradingBotTV/ml_optimizer/requirements.txt
   ```
3. Zbuduj projekt C#:
   ```bash
   dotnet build TradingBotTV/bot/BinanceTraderBot.csproj
   ```
4. W pliku `TradingBotTV/config/settings.json` wpisz klucze API i parametry
   strategii. Możesz też ustawić zmienne `BINANCE_API_KEY` i
   `BINANCE_API_SECRET` w `.env`. Ścieżkę do pliku konfiguracyjnego można
   nadpisać zmienną `BOT_CONFIG_FILE` (oraz `BOT_ENV_FILE` dla alternatywnego
   `.env`). Dodatkowo panel oraz webhook zabezpieczysz zmiennymi
   `DASHBOARD_USERNAME`, `DASHBOARD_PASSWORD` i `WEBHOOK_TOKEN`.
5. Uruchom bota poleceniem:
   ```bash
   dotnet run --project TradingBotTV/bot/BinanceTraderBot.csproj
   ```

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
    "initialCapital": 1000,
    "rsiBuyThreshold": 30,
    "rsiSellThreshold": 70,
    "stopLossPercent": 1.5,
    "takeProfitPercent": 3.0,
    "trailingStopPercent": 0.5,
    "maxDrawdownPercent": 20,
    "emaShortPeriod": 50,
    "emaLongPeriod": 200
  },
  "websocket": {
    "binanceUrl": "wss://stream.binance.com:9443/ws",
    "tradingViewUrl": ""
  }
}
```

- `symbol` – domyślna para handlowa.
- `amount` – ilość kupowana/sprzedawana w pojedynczej transakcji.
- `initialCapital` – początkowy kapitał używany do obliczania wielkości pozycji.
- `rsiBuyThreshold` i `rsiSellThreshold` – progi RSI wykorzystywane w strategii.
- `stopLossPercent` i `takeProfitPercent` – ustawienia SL/TP w procentach.
- `trailingStopPercent` – wielkość trailing stopu aktualizowana po każdej zmianie ceny.
- `maxDrawdownPercent` – maksymalny dopuszczalny spadek wartości portfela (w % od początkowego kapitału), po którego przekroczeniu handel zostaje automatycznie wstrzymany.
- `emaShortPeriod` i `emaLongPeriod` – okresy obliczania krótkiej i długiej EMA używane w filtrze trendu.

- `websocket.binanceUrl` – adres WebSocket Binance z którego pobierane są dane na żywo.
- `websocket.tradingViewUrl` – opcjonalny adres WebSocket z alertami TradingView.

Optymalizatory Pythona mogą modyfikować te wartości automatycznie (zapis w `model_state.json` i aktualizacja przez `OptimizerRunner`).

Bot monitoruje również błędy krytyczne. Jeśli podczas wysyłania zlecenia wystąpi poważny problem, wszystkie otwarte pozycje są natychmiast zamykane, a wielkość kolejnych zleceń obliczana jest dynamicznie na podstawie aktualnego stanu kapitału.
Dodatkowo, moduły Pythona zapisują logi w pliku `TradingBotTV/ml_optimizer/state/ml_optimizer.log`, a wybrane metryki (np. wynik PnL optymalizatora) trafiają do `TradingBotTV/ml_optimizer/state/metrics.csv`. Pobieranie danych i inne zapytania sieciowe są powtarzane kilkukrotnie z narastającym opóźnieniem, co minimalizuje ryzyko błędów sieci.

## Panel WWW

Po uruchomieniu aplikacji dostępny jest prosty panel pod adresem `http://localhost:5001`.
Jeśli ustawisz zmienne `DASHBOARD_USERNAME` i `DASHBOARD_PASSWORD`, panel
poprosi o podanie danych logowania. Znajdziesz tam kafelki z podsumowaniem PnL,
wielkości pozycji oraz przycisk do włączania i wyłączania handlu. Możesz
również podejrzeć ostatni log transakcji.

## Jak uruchomić testy

1. Zainstaluj zależności Pythona i `flake8`:
   ```bash
   pip install -r TradingBotTV/ml_optimizer/requirements.txt
   pip install flake8
   ```
   Jeśli pojawi się błąd związany z brakiem dostępu do `pypi.org`, skonfiguruj
   proxy lub użyj lokalnych plików `.whl`. Łączność sprawdzisz poleceniem:
   `python -m TradingBotTV.ml_optimizer.network_utils https://pypi.org`
2. Uruchom testy: `pytest`
3. Sprawdź styl kodu: `flake8`

Pliki w C# wymagają .NET 8. Informacje o budowaniu i uruchamianiu znajdują się w głównym pliku `README.md`.

## Licencja

Projekt jest dostępny na licencji MIT. Treść licencji znajduje się w pliku
[`LICENSE`](../LICENSE).

