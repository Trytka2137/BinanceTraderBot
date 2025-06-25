using System;
using System.Threading.Tasks;

namespace Bot
{
    class Program
    {
        static async Task Main(string[] args)
        {
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
            Task.Run(() => WebhookServer.Start());
            Task.Run(() => StrategyEngine.StartAsync());
            Task.Run(() => BinanceWebSocket.StartAsync());
            Task.Run(() => TradingViewWebSocket.StartAsync());
            Task.Run(() => DashboardServer.Start());

            // Uruchamiamy kilka pętli optymalizacji w różnych odstępach czasu
            var optTasks = new[]
            {
                RunOptimizerLoop(TimeSpan.FromMinutes(15)),
                RunOptimizerLoop(TimeSpan.FromMinutes(30)),
                RunOptimizerLoop(TimeSpan.FromHours(1)),
                RunTradingViewLoop(TimeSpan.FromMinutes(10))
            };

            await Task.WhenAll(optTasks);
        }

        private static async Task RunOptimizerLoop(TimeSpan interval)
        {
            while (true)
            {
                BotLogger.Log($"🧠 ({interval}) Uruchamiam optymalizację ML...");
                await OptimizerRunner.RunOptimizationAndReloadAsync(ConfigManager.Symbol).ConfigureAwait(false);

                BotLogger.Log($"⏳ Czekam {interval} na kolejną optymalizację...");
                await Task.Delay(interval).ConfigureAwait(false);
            }
        }

        private static async Task RunTradingViewLoop(TimeSpan interval)
        {
            while (true)
            {
                await OptimizerRunner.RunTradingViewAutoTradeAsync(ConfigManager.Symbol).ConfigureAwait(false);
                await Task.Delay(interval).ConfigureAwait(false);
            }
        }
    }
}
