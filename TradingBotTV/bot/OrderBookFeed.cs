using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace Bot
{
    public static class OrderBookFeed
    {
        public static async Task StartAsync(CancellationToken token)
        {
            var attempt = 0;
            while (!token.IsCancellationRequested)
            {
                using var ws = new ClientWebSocket();
                try
                {
                    var url = $"{ConfigManager.BinanceWsUrl}/{ConfigManager.Symbol.ToLower()}@depth@100ms";
                    await ws.ConnectAsync(new Uri(url), token);
                    attempt = 0;
                    Console.WriteLine($"🔌 Połączono z Binance depth WS: {url}");
                    var buffer = new byte[8192];
                    while (ws.State == WebSocketState.Open && !token.IsCancellationRequested)
                    {
                        var result = await ws.ReceiveAsync(buffer, token);
                        if (result.MessageType == WebSocketMessageType.Close)
                        {
                            await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, token);
                            break;
                        }
                        var msg = Encoding.UTF8.GetString(buffer, 0, result.Count);
                        var json = JObject.Parse(msg);
                        var bids = json["bids"]?.Take(5).Select(b => decimal.Parse(b[1].ToString())).ToList() ?? new List<decimal>();
                        var asks = json["asks"]?.Take(5).Select(a => decimal.Parse(a[1].ToString())).ToList() ?? new List<decimal>();
                        var bidSum = bids.Sum();
                        var askSum = asks.Sum();
                        var total = bidSum + askSum;
                        if (total > 0)
                        {
                            var imbalance = (bidSum - askSum) / total;
                            int signal = 0;
                            if (imbalance > 0.1m) signal = 1;
                            else if (imbalance < -0.1m) signal = -1;
                            StrategyEngine.UpdateHftSignal(signal);
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd WebSocket order book: {ex.Message}");
                    attempt++;
                }
                var delay = TimeSpan.FromSeconds(Math.Min(300, Math.Pow(2, attempt)));
                Console.WriteLine($"↺ Ponawiam order book za {delay.TotalSeconds:F0}s...");
                await Task.Delay(delay, token).ConfigureAwait(false);
            }
        }
    }
}
