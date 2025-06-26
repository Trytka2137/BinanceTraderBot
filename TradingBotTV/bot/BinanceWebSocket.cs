using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Bot
{
    public static class BinanceWebSocket
    {
        public static async Task StartAsync(CancellationToken token)
        {
            var attempt = 0;
            while (!token.IsCancellationRequested)
            {
                using var ws = new ClientWebSocket();
                try
                {
                    var url = $"{ConfigManager.BinanceWsUrl}/{ConfigManager.Symbol.ToLower()}@ticker";
                    await ws.ConnectAsync(new Uri(url), token);
                    attempt = 0;
                    Console.WriteLine($"\uD83D\uDD0C Połączono z Binance WS: {url}");
                    var buffer = new byte[4096];
                    while (ws.State == WebSocketState.Open && !token.IsCancellationRequested)
                    {
                        var result = await ws.ReceiveAsync(buffer, token);
                        if (result.MessageType == WebSocketMessageType.Close)
                        {
                            await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, token);
                            break;
                        }
                        var msg = Encoding.UTF8.GetString(buffer, 0, result.Count);
                        Console.WriteLine($"\uD83C\uDF10 Binance: {msg}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd WebSocket Binance: {ex.Message}");
                    attempt++;
                }
                var delay = TimeSpan.FromSeconds(Math.Min(300, Math.Pow(2, attempt)));
                Console.WriteLine($"↺ Ponawiam połączenie z Binance za {delay.TotalSeconds:F0}s...");
                await Task.Delay(delay, token).ContinueWith(_ => { });
            }
        }
    }
}
