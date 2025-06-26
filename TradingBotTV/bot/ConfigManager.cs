using System;
using System.IO;
using Newtonsoft.Json.Linq;

namespace Bot
{
    public static class ConfigManager
    {
        private static readonly string _filePath =
            Path.Combine(AppContext.BaseDirectory, "config", "settings.json");
        private static readonly string _envPath =
            Path.Combine(AppContext.BaseDirectory, ".env");
        private static JObject _config;

        public static void Load()
        {
            LoadEnvFile();
            if (!File.Exists(_filePath))
                throw new FileNotFoundException($"Config file not found: {_filePath}");

            var text = File.ReadAllTextAsync(_filePath).GetAwaiter().GetResult();
            _config = JObject.Parse(text);
            Validate();
        }

        private static void LoadEnvFile()
        {
            if (!File.Exists(_envPath))
                return;

            foreach (var line in File.ReadAllLines(_envPath))
            {
                var trimmed = line.Trim();
                if (string.IsNullOrWhiteSpace(trimmed) || trimmed.StartsWith("#"))
                    continue;

                var parts = trimmed.Split('=', 2);
                if (parts.Length == 2)
                    Environment.SetEnvironmentVariable(parts[0].Trim(), parts[1].Trim());
            }
        }

        private static void Validate()
        {
            var trading = _config["trading"] as JObject;
            if (trading == null)
                return;

            void CheckPercent(string name)
            {
                if (trading[name] != null)
                {
                    decimal value = (decimal)trading[name];
                    if (value < 0 || value > 100)
                        throw new ArgumentOutOfRangeException(name, $"{name} must be between 0 and 100");
                }
            }

            CheckPercent("stopLossPercent");
            CheckPercent("takeProfitPercent");
            CheckPercent("trailingStopPercent");
            CheckPercent("maxDrawdownPercent");

            if (trading["amount"] != null && (decimal)trading["amount"] <= 0)
                throw new ArgumentOutOfRangeException("amount", "amount must be positive");
        }

        public static string ApiKey =>
            Environment.GetEnvironmentVariable("BINANCE_API_KEY")
            ?? _config["binance"]["apiKey"].ToString();

        public static string ApiSecret =>
            Environment.GetEnvironmentVariable("BINANCE_API_SECRET")
            ?? _config["binance"]["apiSecret"].ToString();
        public static string Symbol => _config["trading"]["symbol"].ToString();
        public static decimal Amount => (decimal)_config["trading"]["amount"];
        public static decimal InitialCapital =>
            (decimal?)_config["trading"]?["initialCapital"] ?? 1000m;
        public static int RsiBuyThreshold => (int)_config["trading"]["rsiBuyThreshold"];
        public static int RsiSellThreshold => (int)_config["trading"]["rsiSellThreshold"];
        public static decimal StopLossPercent => (decimal)_config["trading"]["stopLossPercent"];
        public static decimal TakeProfitPercent => (decimal)_config["trading"]["takeProfitPercent"];
        public static decimal TrailingStopPercent => (decimal?)_config["trading"]?["trailingStopPercent"] ?? 0.5m;
        public static decimal MaxDrawdownPercent => (decimal?)_config["trading"]?["maxDrawdownPercent"] ?? 20m;
        public static int EmaShortPeriod => (int?)_config["trading"]?["emaShortPeriod"] ?? 50;
        public static int EmaLongPeriod => (int?)_config["trading"]?["emaLongPeriod"] ?? 200;
        public static string BinanceWsUrl =>
            _config["websocket"]?["binanceUrl"]?.ToString() ?? "wss://stream.binance.com:9443/ws";
        public static string TradingViewWsUrl =>
            _config["websocket"]?["tradingViewUrl"]?.ToString() ?? string.Empty;

        public static void Reload() => Load();

        public static void OverrideSymbol(string symbol)
        {
            _config["trading"]["symbol"] = symbol;
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(_filePath)!);
                File.WriteAllTextAsync(_filePath, _config.ToString()).GetAwaiter().GetResult();
            }
            catch
            {
                // ignore save errors
            }
        }
    }
}
