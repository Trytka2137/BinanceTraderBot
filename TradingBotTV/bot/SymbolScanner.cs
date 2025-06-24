using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Bot
{
    public static class SymbolScanner
    {
        public static async Task<List<string>> GetTradingPairsAsync()
        {
            var pairs = new List<string>();
            try
            {
                using var client = new HttpClient();
                var response = await client.GetStringAsync("https://api.binance.com/api/v3/exchangeInfo");
                var json = JObject.Parse(response);

                foreach (var symbol in json["symbols"])
                {
                    if (symbol["quoteAsset"].ToString() == "USDT" && symbol["status"].ToString() == "TRADING")
                        pairs.Add(symbol["symbol"].ToString());
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Błąd pobierania listy par: {ex.Message}");
            }

            return pairs;
        }

        public static async Task<string?> GetHighestVolumePairAsync(IEnumerable<string> pairs)
        {
            const int maxPairsToCheck = 50;   // limit number of pairs processed
            const int maxConcurrentRequests = 5; // avoid hitting API rate limits

            var limitedPairs = pairs.Take(maxPairsToCheck).ToList();
            using var client = new HttpClient();
            using var semaphore = new SemaphoreSlim(maxConcurrentRequests);

            var tasks = limitedPairs.Select(async p =>
            {
                await semaphore.WaitAsync();
                try
                {
                    var resp = await client.GetStringAsync($"https://api.binance.com/api/v3/ticker/24hr?symbol={p}");
                    var obj = JObject.Parse(resp);
                    var vol = decimal.Parse(obj["quoteVolume"].ToString());
                    return (pair: p, volume: vol);
                }
                catch
                {
                    return (pair: p, volume: 0m);
                }
                finally
                {
                    semaphore.Release();
                }
            }).ToArray();

            var results = await Task.WhenAll(tasks);

            var best = results.OrderByDescending(r => r.volume).FirstOrDefault();
            return best.volume > 0 ? best.pair : null;
        }
    }
}
