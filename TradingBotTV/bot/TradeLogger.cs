using System;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Threading.Tasks;

namespace Bot
{
    public static class TradeLogger
    {
        private static readonly string _logPath =
            Path.Combine(AppContext.BaseDirectory, "data", "trade_log.csv");
        public static string LogPath => _logPath;
        private static readonly object _lock = new object();

        public static void LogTrade(string symbol, string side, decimal price, decimal amount)
        {
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(LogPath)!);
                var line = string.Join(',',
                    DateTime.UtcNow.ToString("o"),
                    symbol,
                    side,
                    price.ToString(CultureInfo.InvariantCulture),
                    amount.ToString(CultureInfo.InvariantCulture));
                lock (_lock)
                {
                    File.AppendAllText(LogPath, line + Environment.NewLine);
                }
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
                    if (!decimal.TryParse(parts[3], NumberStyles.Any, CultureInfo.InvariantCulture, out var price))
                        continue;
                    if (!decimal.TryParse(parts[4], NumberStyles.Any, CultureInfo.InvariantCulture, out var amount))
                        continue;
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

        public static decimal GetNetPosition()
        {
            try
            {
                if (!File.Exists(LogPath))
                    return 0m;
                var lines = File.ReadAllLines(LogPath);
                decimal net = 0m;
                foreach (var l in lines)
                {
                    var parts = l.Split(',');
                    if (parts.Length < 5)
                        continue;
                    var side = parts[2];
                    if (!decimal.TryParse(parts[4], NumberStyles.Any, CultureInfo.InvariantCulture, out var amount))
                        continue;
                    if (side.Equals("BUY", StringComparison.OrdinalIgnoreCase))
                        net += amount;
                    else if (side.Equals("SELL", StringComparison.OrdinalIgnoreCase))
                        net -= amount;
                }
                return net;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd obliczania pozycji netto: {ex.Message}");
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
                var output = await process.StandardOutput.ReadToEndAsync().ConfigureAwait(false);
                var error = await process.StandardError.ReadToEndAsync().ConfigureAwait(false);
                await process.WaitForExitAsync().ConfigureAwait(false);

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
