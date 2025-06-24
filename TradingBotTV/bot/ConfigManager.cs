using System.IO;
using Newtonsoft.Json.Linq;

namespace Bot
{
    public static class ConfigManager
    {
        private static string _filePath = "config/settings.json";
        private static JObject _config;

        public static void Load()
        {
            var text = File.ReadAllText(_filePath);
            _config = JObject.Parse(text);
        }

        public static string ApiKey => _config["binance"]["apiKey"].ToString();
        public static string ApiSecret => _config["binance"]["apiSecret"].ToString();
        public static string Symbol => _config["trading"]["symbol"].ToString();
        public static decimal Amount => (decimal)_config["trading"]["amount"];
        public static int RsiBuyThreshold => (int)_config["trading"]["rsiBuyThreshold"];
        public static int RsiSellThreshold => (int)_config["trading"]["rsiSellThreshold"];
        public static decimal StopLossPercent => (decimal)_config["trading"]["stopLossPercent"];
        public static decimal TakeProfitPercent => (decimal)_config["trading"]["takeProfitPercent"];

        public static void Reload() => Load();
    }
}
