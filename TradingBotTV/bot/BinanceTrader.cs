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
        private static readonly HttpClient httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(10)
        };

        public BinanceTrader()
        {
            ConfigManager.Load();
            apiKey = ConfigManager.ApiKey;
            apiSecret = ConfigManager.ApiSecret;
            defaultSymbol = ConfigManager.Symbol;
        }

        public async Task ExecuteTrade(string signal, string? symbolOverride = null)
        {
            if (!BotController.TradingEnabled)
            {
                Console.WriteLine("⏸️ Trading is disabled – zlecenie pominięte.");
                return;
            }
            var symbol = symbolOverride ?? defaultSymbol;

            var side = signal.ToUpper(); // BUY or SELL

            // Oblicz stop loss i take profit na podstawie bieżącej ceny
            var price = await GetCurrentPrice(symbol).ConfigureAwait(false);
            if (price <= 0)
            {
                Console.WriteLine($"❌ Nie udało się pobrać ceny dla {symbol}");
                return;
            }
            var sl = price * (1 - ConfigManager.StopLossPercent / 100m);
            var tp = price * (1 + ConfigManager.TakeProfitPercent / 100m);

            var quantity = PositionSizer.GetTradeAmount(price, side);

            if (quantity <= 0)
            {
                Console.WriteLine("❌ Ilość zlecenia wynosi 0 – przerwano");
                return;
            }

            var request = new HttpRequestMessage(HttpMethod.Post, GetOrderUrl(symbol, side, quantity));
            request.Headers.Add("X-MBX-APIKEY", apiKey);

            Console.WriteLine($"🚀 Wysyłam zlecenie {side} {quantity} {symbol} (SL={sl:F2}, TP={tp:F2})");

            try
            {
                var response = await httpClient.SendAsync(request).ConfigureAwait(false);
                var content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);

                if (!response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"❌ Błąd API {response.StatusCode}: {content}");
                }
                else
                {
                    Console.WriteLine($"✅ Binance Response: {content}");
                    TradeLogger.LogTrade(symbol, side, price, quantity);
                    var pnl = TradeLogger.AnalyzePnL();
                    Console.WriteLine($"\uD83D\uDCC8 Aktualny wynik: {pnl:F2}");
                    await TradeLogger.CompareWithStrategiesAsync(symbol).ConfigureAwait(false);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd wysyłania zlecenia: {ex.Message}");
                await CloseAllPositionsAsync().ConfigureAwait(false);
            }
        }

        private static async Task<decimal> GetCurrentPrice(string symbol)
        {
            var url = $"https://api.binance.com/api/v3/ticker/price?symbol={symbol}";
            try
            {
                var json = await httpClient.GetStringAsync(url).ConfigureAwait(false);
                var obj = Newtonsoft.Json.Linq.JObject.Parse(json);
                return decimal.Parse(obj["price"].ToString());
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd pobierania ceny: {ex.Message}");
                return 0m;
            }
        }

        private string GetOrderUrl(string symbol, string side, decimal quantity)
        {
            var endpoint = "https://api.binance.com/api/v3/order/test"; // test order for safety
            var timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            var query = $"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}";
            return $"{endpoint}?{query}";
        }

        private string GetOrderUrl(string symbol, string signal)
        {
            return GetOrderUrl(symbol, signal.ToUpper(), ConfigManager.Amount);
        }

        private async Task CloseAllPositionsAsync()
        {
            var net = TradeLogger.GetNetPosition();
            if (net == 0) return;
            var side = net > 0 ? "SELL" : "BUY";
            var quantity = Math.Abs(net);
            var price = await GetCurrentPrice(defaultSymbol).ConfigureAwait(false);
            var request = new HttpRequestMessage(HttpMethod.Post, GetOrderUrl(defaultSymbol, side, quantity));
            request.Headers.Add("X-MBX-APIKEY", apiKey);
            try
            {
                var response = await httpClient.SendAsync(request).ConfigureAwait(false);
                var content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
                if (!response.IsSuccessStatusCode)
                    Console.WriteLine($"❌ Błąd zamykania pozycji: {response.StatusCode}: {content}");
                else
                {
                    Console.WriteLine($"⚠️ Zamknięto wszystkie pozycje: {content}");
                    TradeLogger.LogTrade(defaultSymbol, side, price, quantity);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd wysyłania zlecenia zamykającego: {ex.Message}");
            }
        }
    }
}
