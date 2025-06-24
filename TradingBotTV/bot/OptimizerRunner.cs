using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

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
                psi.Arguments = $"ml_optimizer/optimizer.py {symbol}";
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
                // Załóżmy, że output zawiera linię: BestParams: buy=30 sell=70
                var lines = output.Split('\n');
                foreach (var line in lines)
                {
                    if (line.StartsWith("Najlepsze parametry:"))
                    {
                        var parts = line.Split(new string[] { "Buy=", "Sell=", "," }, StringSplitOptions.RemoveEmptyEntries);
                        if(parts.Length >= 3)
                        {
                            int buyTh = int.Parse(parts[1].Trim());
                            int sellTh = int.Parse(parts[2].Trim());

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
    }
}
