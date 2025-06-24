using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace Bot
{
    public static class StrategyEngine
    {
        private static readonly HttpClient client = new HttpClient();

        public static async Task StartAsync()
        {
            while (true)
            {
                try
                {
                    var prices = await FetchCloses(ConfigManager.Symbol, 50);
                    if (prices.Count >= 15)
                    {
                        var rsi = ComputeRsi(prices);
                        if (rsi < ConfigManager.RsiBuyThreshold)
                        {
                            var trader = new BinanceTrader();
                            await trader.ExecuteTrade("BUY");
                        }
                        else if (rsi > ConfigManager.RsiSellThreshold)
                        {
                            var trader = new BinanceTrader();
                            await trader.ExecuteTrade("SELL");
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd strategii: {ex.Message}");
                }

                await Task.Delay(TimeSpan.FromMinutes(1));
            }
        }

        private static async Task<List<decimal>> FetchCloses(string symbol, int limit)
        {
            var url = $"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}";
            var json = await client.GetStringAsync(url);
            var arr = JArray.Parse(json);
            return arr.Select(x => decimal.Parse(x[4].ToString())).ToList();
        }

        private static decimal ComputeRsi(List<decimal> closes, int period = 14)
        {
            var gains = new List<decimal>();
            var losses = new List<decimal>();
            for (int i = 1; i < closes.Count; i++)
            {
                var diff = closes[i] - closes[i - 1];
                if (diff >= 0)
                {
                    gains.Add(diff);
                    losses.Add(0);
                }
                else
                {
                    gains.Add(0);
                    losses.Add(-diff);
                }
            }
            var avgGain = gains.Take(period).Average();
            var avgLoss = losses.Take(period).Average();
            for (int i = period; i < gains.Count; i++)
            {
                avgGain = (avgGain * (period - 1) + gains[i]) / period;
                avgLoss = (avgLoss * (period - 1) + losses[i]) / period;
            }
            if (avgLoss == 0) return 100;
            var rs = avgGain / avgLoss;
            var rsi = 100 - (100 / (1 + rs));
            return decimal.Round((decimal)rsi, 2);
        }
    }
}
