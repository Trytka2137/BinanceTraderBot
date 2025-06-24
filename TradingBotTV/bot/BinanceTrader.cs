using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace Bot
{
    public class BinanceTrader
    {
        private readonly string apiKey;
        private readonly string apiSecret;
        private readonly string defaultSymbol;
        private readonly decimal amount;

        public BinanceTrader()
        {
            ConfigManager.Load();
            apiKey = ConfigManager.ApiKey;
            apiSecret = ConfigManager.ApiSecret;
            defaultSymbol = ConfigManager.Symbol;
            amount = ConfigManager.Amount;
        }

        public async Task ExecuteTrade(string signal, string? symbolOverride = null)
        {
            var symbol = symbolOverride ?? defaultSymbol;
            using var client = new HttpClient();
            client.DefaultRequestHeaders.Add("X-MBX-APIKEY", apiKey);

            var side = signal.ToUpper(); // BUY or SELL
            var endpoint = "https://api.binance.com/api/v3/order/test"; // test order for safety

            var timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            var query = $"symbol={symbol}&side={side}&type=MARKET&quantity={amount}&timestamp={timestamp}";

            var url = $"{endpoint}?{query}";

            // Oblicz stop loss i take profit na podstawie bieżącej ceny
            var price = await GetCurrentPrice(symbol);
            var sl = price * (1 - ConfigManager.StopLossPercent / 100m);
            var tp = price * (1 + ConfigManager.TakeProfitPercent / 100m);

            Console.WriteLine($"🚀 Wysyłam zlecenie {side} {amount} {symbol} (SL={sl:F2}, TP={tp:F2})");

            try
            {
                var response = await client.PostAsync(url, null);
                var content = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"❌ Błąd API {response.StatusCode}: {content}");
                }
                else
                {
                    Console.WriteLine($"✅ Binance Response: {content}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd wysyłania zlecenia: {ex.Message}");
            }
        }

        private async Task<decimal> GetCurrentPrice(string symbol)
        {
            using var client = new HttpClient();
            var url = $"https://api.binance.com/api/v3/ticker/price?symbol={symbol}";
            var json = await client.GetStringAsync(url);
            var obj = Newtonsoft.Json.Linq.JObject.Parse(json);
            return decimal.Parse(obj["price"].ToString());
        }
    }
}
