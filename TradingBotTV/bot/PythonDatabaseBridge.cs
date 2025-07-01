using System;
using System.Diagnostics;
using System.Globalization;
using System.Threading.Tasks;

namespace Bot
{
    public static class PythonDatabaseBridge
    {
        private static async Task RunAsync(string args)
        {
            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"-m TradingBotTV.ml_optimizer.db_cli {args}",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            using var process = Process.Start(psi);
            if (process == null) return;
            await process.WaitForExitAsync().ConfigureAwait(false);
        }

        public static Task InitDbAsync() => RunAsync("init");

        public static Task StoreTradeAsync(string timestamp, string symbol, string side, decimal qty, decimal price)
        {
            string q = qty.ToString(CultureInfo.InvariantCulture);
            string p = price.ToString(CultureInfo.InvariantCulture);
            return RunAsync($"trade \"{timestamp}\" \"{symbol}\" \"{side}\" {q} {p}");
        }

        public static Task StoreMetricAsync(string timestamp, string name, decimal value)
        {
            string v = value.ToString(CultureInfo.InvariantCulture);
            return RunAsync($"metric \"{timestamp}\" \"{name}\" {v}");
        }
    }
}
