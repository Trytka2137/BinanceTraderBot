using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace Bot
{
    public static class TradeLogger
    {
        private static readonly string LogPath =
            Path.Combine(AppContext.BaseDirectory, "data", "trade_log.csv");

        public static void LogTrade(string symbol, string side, decimal price, decimal amount)
        {
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(LogPath)!);
                var line = $"{DateTime.UtcNow:o},{symbol},{side},{price},{amount}";
                File.AppendAllText(LogPath, line + Environment.NewLine);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd zapisu trade logu: {ex.Message}");
            }
        }

        public static decimal AnalyzePnL()
        {
            try
            {
                if (!File.Exists(LogPath))
                    return 0m;
                var lines = File.ReadAllLines(LogPath);
                decimal pnl = 0m;
                decimal? lastBuyPrice = null;
                decimal lastAmount = 0m;
                foreach (var l in lines)
                {
                    var parts = l.Split(',');
                    if (parts.Length < 5)
                        continue;
                    var side = parts[2];
                    var price = decimal.Parse(parts[3]);
                    var amount = decimal.Parse(parts[4]);
                    if (side.Equals("BUY", StringComparison.OrdinalIgnoreCase))
                    {
                        lastBuyPrice = price;
                        lastAmount = amount;
                    }
                    else if (side.Equals("SELL", StringComparison.OrdinalIgnoreCase) && lastBuyPrice.HasValue)
                    {
                        pnl += (price - lastBuyPrice.Value) * lastAmount;
                        lastBuyPrice = null;
                    }
                }
                return pnl;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd analizy PnL: {ex.Message}");
                return 0m;
            }
        }

        public static async Task CompareWithStrategiesAsync(string symbol)
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"ml_optimizer/compare_strategies.py {symbol}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    WorkingDirectory = Path.Combine(AppContext.BaseDirectory, "..")
                };
                using var process = Process.Start(psi);
                if (process == null) return;
                var output = await process.StandardOutput.ReadToEndAsync();
                var error = await process.StandardError.ReadToEndAsync();
                await process.WaitForExitAsync();

                Console.WriteLine("\uD83D\uDCCA Wyniki porównania strategii:");
                Console.WriteLine(output);
                if (!string.IsNullOrEmpty(error))
                    Console.WriteLine("⚠️ Błędy porównania strategii: " + error);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd uruchamiania porównania strategii: {ex.Message}");
            }
        }
    }
}
