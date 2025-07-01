using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading;
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

        private static int _hftSignal;

        public static void UpdateHftSignal(int signal)
        {
            _hftSignal = signal;
        }

        private static decimal ComputeVolatility(List<decimal> closes)
        {
            if (closes.Count < 2) return 0m;
            var mean = closes.Average();
            var variance = closes.Select(c => (c - mean) * (c - mean)).Average();
            return Math.Round((decimal)Math.Sqrt((double)variance), 4);
        }

        public static async Task StartAsync(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                try
                {
                    var task1m = FetchKlines(ConfigManager.Symbol, 50, "1m");
                    var task30m = FetchKlines(ConfigManager.Symbol, 50, "30m");
                    var task1h = FetchKlines(ConfigManager.Symbol, ConfigManager.EmaLongPeriod, "1h");

                    await Task.WhenAll(task1m, task30m, task1h).ConfigureAwait(false);

                    var klines1m = task1m.Result;
                    var klines30m = task30m.Result;
                    var klines1h = task1h.Result;

                    if (klines1m.Count >= 15 && klines30m.Count >= 15 && klines1h.Count >= 15)
                    {
                        var closes1m = klines1m.Select(k => k.Close).ToList();
                        var closes30m = klines30m.Select(k => k.Close).ToList();
                        var closes1h = klines1h.Select(k => k.Close).ToList();
                        var volumes = klines1m.Select(k => k.Volume).ToList();

                        var rsi1m = ComputeRsi(closes1m);
                        var rsi30m = ComputeRsi(closes30m);
                        var rsi1h = ComputeRsi(closes1h);
                        var emaShort = ComputeEma(closes1h, ConfigManager.EmaShortPeriod);
                        var emaLong = ComputeEma(closes1h, ConfigManager.EmaLongPeriod);
                        var volatility = ComputeVolatility(closes1m);
                        var volFactor = ComputeVolumeFactor(volumes);

                        bool uptrend = emaShort > emaLong;
                        bool downtrend = emaShort < emaLong;

                        if (rsi1m < ConfigManager.RsiBuyThreshold &&
                            rsi30m < ConfigManager.RsiBuyThreshold &&
                            rsi1h < ConfigManager.RsiBuyThreshold &&
                            volFactor > 1.2m && uptrend && _hftSignal > 0)
                        {
                            var trader = new BinanceTrader();
                            await trader.ExecuteTrade("BUY", null, volatility).ConfigureAwait(false);
                        }
                        else if (rsi1m > ConfigManager.RsiSellThreshold &&
                                 rsi30m > ConfigManager.RsiSellThreshold &&
                                 rsi1h > ConfigManager.RsiSellThreshold &&
                                 volFactor > 1.2m && downtrend && _hftSignal < 0)
                        {
                            var trader = new BinanceTrader();
                            await trader.ExecuteTrade("SELL", null, volatility).ConfigureAwait(false);
                        }
                    }
                }
                catch (Exception ex)
                {
                    BotLogger.Log($"❌ Błąd strategii: {ex.Message}");
                }

                await Task.Delay(TimeSpan.FromMinutes(1), token).ConfigureAwait(false);
            }
        }

        private static async Task<List<Kline>> FetchKlines(string symbol, int limit, string interval)
        {
            var url = $"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}";
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

        private static decimal ComputeEma(List<decimal> closes, int period)
        {
            if (closes.Count == 0) return 0m;
            decimal multiplier = 2m / (period + 1);
            decimal ema = closes[0];
            for (int i = 1; i < closes.Count; i++)
            {
                ema = ((closes[i] - ema) * multiplier) + ema;
            }
            return decimal.Round(ema, 4);
        }
    }
}
