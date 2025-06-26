using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

using Newtonsoft.Json.Linq;
namespace Bot
{
    public static class OptimizerRunner
    {
        public static async Task RunOptimizationAndReloadAsync(string symbol)
        {
            try
            {
                var psi = new ProcessStartInfo();
                psi.FileName = "python";
                psi.Arguments = $"ml_optimizer/auto_optimizer.py {symbol}";
                psi.RedirectStandardOutput = true;
                psi.RedirectStandardError = true;
                psi.UseShellExecute = false;
                psi.CreateNoWindow = true;

                using var process = Process.Start(psi);

                string output = await process.StandardOutput.ReadToEndAsync();
                string error = await process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync();

                Console.WriteLine("🧠 Optymalizacja ML output:");
                Console.WriteLine(output);
                if (!string.IsNullOrEmpty(error))
                    Console.WriteLine("⚠️ Błędy optymalizacji: " + error);

                // Parsujemy output, żeby uaktualnić config:
                // Szukamy linii w formacie "Najlepsze parametry: Buy=30 Sell=70 PnL=..."
                foreach (var line in output.Split('\n'))
                {
                    if (line.StartsWith("Najlepsze parametry:"))
                    {
                        var match = Regex.Match(line, @"Buy=(\d+).*Sell=(\d+)");
                        if (match.Success)
                        {
                            int buyTh = int.Parse(match.Groups[1].Value);
                            int sellTh = int.Parse(match.Groups[2].Value);
                            UpdateConfig(buyTh, sellTh);
                            Console.WriteLine($"♻️ Zaktualizowano ustawienia RSI: Buy={buyTh}, Sell={sellTh}");
                        }
                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("❌ Błąd uruchamiania optymalizacji: " + ex.Message);
            }
        }

        private static void UpdateConfig(int buyTh, int sellTh)
        {
            string path = "config/settings.json";
            var json = File.ReadAllText(path);
            var obj = JObject.Parse(json);
            obj["trading"]["rsiBuyThreshold"] = buyTh;
            obj["trading"]["rsiSellThreshold"] = sellTh;
            File.WriteAllText(path, obj.ToString());
            ConfigManager.Reload();
        }

        public static async Task RunTradingViewAutoTradeAsync(string symbol)
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"ml_optimizer/tradingview_auto_trader.py {symbol}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                using var process = Process.Start(psi);
                if (process == null) return;
                string output = await process.StandardOutput.ReadToEndAsync();
                string error = await process.StandardError.ReadToEndAsync();
                await process.WaitForExitAsync();
                BotLogger.Log("📈 TradingView auto trader output:");
                BotLogger.Log(output.Trim());
                if (!string.IsNullOrEmpty(error))
                    BotLogger.Log("⚠️ TradingView errors: " + error);
            }
            catch (Exception ex)
            {
                BotLogger.Log("❌ Błąd TradingView auto trader: " + ex.Message);
            }
        }
    }
}
