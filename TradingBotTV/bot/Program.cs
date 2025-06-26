using System;
using System.Threading;
using System.Threading.Tasks;

namespace Bot
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.CancelKeyPress += (s, e) =>
            {
                e.Cancel = true;
                AppLifetime.Source.Cancel();
            };

            BotLogger.Log("🚀 Bot uruchomiony. Oczekuję na sygnały z TradingView...");

            ConfigManager.Load();

            var pairs = await SymbolScanner.GetTradingPairsAsync().ConfigureAwait(false);
            var best = await SymbolScanner.GetHighestVolumePairAsync(pairs).ConfigureAwait(false);
            if (!string.IsNullOrEmpty(best))
            {
                BotLogger.Log($"\uD83D\uDCCA Wybrano par\u0119 o najwy\u017Cszej likwidno\u015Bci: {best}");
                ConfigManager.OverrideSymbol(best);
            }

            // Start serwera webhook, silnika strategii oraz WebSocketów w tle
            var token = AppLifetime.Source.Token;
            Task.Run(() => WebhookServer.Start(token));
            Task.Run(() => StrategyEngine.StartAsync(token));
            Task.Run(() => BinanceWebSocket.StartAsync(token));
            Task.Run(() => TradingViewWebSocket.StartAsync(token));
            Task.Run(() => DashboardServer.Start(token));

            // Uruchamiamy kilka pętli optymalizacji w różnych odstępach czasu
            var optTasks = new[]
            {
                RunOptimizerLoop(TimeSpan.FromMinutes(15), token),
                RunOptimizerLoop(TimeSpan.FromMinutes(30), token),
                RunOptimizerLoop(TimeSpan.FromHours(1), token),
                RunTradingViewLoop(TimeSpan.FromMinutes(10), token)
            };

            await Task.WhenAll(optTasks);
        }

        private static async Task RunOptimizerLoop(TimeSpan interval, CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                BotLogger.Log($"🧠 ({interval}) Uruchamiam optymalizację ML...");
                await OptimizerRunner.RunOptimizationAndReloadAsync(ConfigManager.Symbol).ConfigureAwait(false);

                BotLogger.Log($"⏳ Czekam {interval} na kolejną optymalizację...");
                await Task.Delay(interval, token).ConfigureAwait(false);
            }
        }

        private static async Task RunTradingViewLoop(TimeSpan interval, CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                await OptimizerRunner.RunTradingViewAutoTradeAsync(ConfigManager.Symbol).ConfigureAwait(false);
                await Task.Delay(interval, token).ConfigureAwait(false);
            }
        }
    }
}
