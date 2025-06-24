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
            using var client = new HttpClient();
            var response = await client.GetStringAsync("https://api.binance.com/api/v3/exchangeInfo");
            var json = JObject.Parse(response);
            var pairs = new List<string>();

            foreach (var symbol in json["symbols"])
            {
                if (symbol["quoteAsset"].ToString() == "USDT" && symbol["status"].ToString() == "TRADING")
                    pairs.Add(symbol["symbol"].ToString());
            }
            return pairs;
        }
    }
}
