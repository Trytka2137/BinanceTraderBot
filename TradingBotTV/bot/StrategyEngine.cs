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
        private static readonly HttpClient client = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(10)
        };

        private record Kline(decimal Close, decimal Volume);

        public static async Task StartAsync()
        {
            while (true)
            {
                try
                {
                    var klines = await FetchKlines(ConfigManager.Symbol, 50).ConfigureAwait(false);
                    if (klines.Count >= 15)
                    {
                        var closes = klines.Select(k => k.Close).ToList();
                        var volumes = klines.Select(k => k.Volume).ToList();
                        var rsi = ComputeRsi(closes);
                        var volFactor = ComputeVolumeFactor(volumes);
                        if (rsi < ConfigManager.RsiBuyThreshold && volFactor > 1.2m)
                        {
                            var trader = new BinanceTrader();
                            await trader.ExecuteTrade("BUY").ConfigureAwait(false);
                        }
                        else if (rsi > ConfigManager.RsiSellThreshold && volFactor > 1.2m)
                        {
                            var trader = new BinanceTrader();
                            await trader.ExecuteTrade("SELL").ConfigureAwait(false);
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd strategii: {ex.Message}");
                }

                await Task.Delay(TimeSpan.FromMinutes(1)).ConfigureAwait(false);
            }
        }

        private static async Task<List<Kline>> FetchKlines(string symbol, int limit)
        {
            var url = $"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}";
            var json = await client.GetStringAsync(url).ConfigureAwait(false);
            var arr = JArray.Parse(json);
            var list = new List<Kline>();
            foreach (var x in arr)
            {
                var close = decimal.Parse(x[4].ToString());
                var volume = decimal.Parse(x[5].ToString());
                list.Add(new Kline(close, volume));
            }
            return list;
        }

        private static decimal ComputeVolumeFactor(List<decimal> volumes, int lookback = 20)
        {
            if (volumes.Count < lookback + 1) return 0m;
            var avg = volumes.Skip(volumes.Count - lookback).Average();
            var last = volumes.Last();
            if (avg == 0) return 0m;
            return decimal.Round(last / avg, 2);
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
