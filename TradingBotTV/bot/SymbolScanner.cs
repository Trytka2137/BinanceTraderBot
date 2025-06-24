using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;

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
            string? best = null;
            decimal bestVol = 0m;
            using var client = new HttpClient();
            foreach (var p in pairs)
            {
                try
                {
                    var resp = await client.GetStringAsync($"https://api.binance.com/api/v3/ticker/24hr?symbol={p}");
                    var obj = JObject.Parse(resp);
                    var vol = decimal.Parse(obj["quoteVolume"].ToString());
                    if (vol > bestVol)
                    {
                        bestVol = vol;
                        best = p;
                    }
                }
                catch
                {
                    // ignore
                }
            }
            return best;
        }
    }
}
