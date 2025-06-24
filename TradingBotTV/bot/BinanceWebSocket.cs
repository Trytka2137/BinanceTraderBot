using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Bot
{
    public static class BinanceWebSocket
    {
        public static async Task StartAsync()
        {
            while (true)
            {
                using var ws = new ClientWebSocket();
                try
                {
                    var url = $"{ConfigManager.BinanceWsUrl}/{ConfigManager.Symbol.ToLower()}@ticker";
                    await ws.ConnectAsync(new Uri(url), CancellationToken.None);
                    Console.WriteLine($"\uD83D\uDD0C Połączono z Binance WS: {url}");
                    var buffer = new byte[4096];
                    while (ws.State == WebSocketState.Open)
                    {
                        var result = await ws.ReceiveAsync(buffer, CancellationToken.None);
                        if (result.MessageType == WebSocketMessageType.Close)
                        {
                            await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
                            break;
                        }
                        var msg = Encoding.UTF8.GetString(buffer, 0, result.Count);
                        Console.WriteLine($"\uD83C\uDF10 Binance: {msg}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd WebSocket Binance: {ex.Message}");
                }

                Console.WriteLine("↺ Ponawiam połączenie z Binance za 30s...");
                await Task.Delay(TimeSpan.FromSeconds(30));
            }
        }
    }
}
