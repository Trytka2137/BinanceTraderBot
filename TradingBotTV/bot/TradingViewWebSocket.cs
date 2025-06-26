using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Bot
{
    public static class TradingViewWebSocket
    {
        public static async Task StartAsync(CancellationToken token)
        {
            if (string.IsNullOrEmpty(ConfigManager.TradingViewWsUrl))
            {
                Console.WriteLine("ℹ️ Nie ustawiono adresu TradingView WebSocket.");
                return;
            }

            var attempt = 0;
            while (!token.IsCancellationRequested)
            {
                using var ws = new ClientWebSocket();
                try
                {
                    await ws.ConnectAsync(new Uri(ConfigManager.TradingViewWsUrl), token);
                    attempt = 0;
                    Console.WriteLine("\uD83D\uDD0C Połączono z TradingView WS");
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
                        Console.WriteLine($"\uD83C\uDF10 TradingView: {msg}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd WebSocket TradingView: {ex.Message}");
                    attempt++;
                }

                var delay = TimeSpan.FromSeconds(Math.Min(300, Math.Pow(2, attempt)));
                Console.WriteLine($"↺ Ponawiam połączenie z TradingView za {delay.TotalSeconds:F0}s...");
                await Task.Delay(delay, token).ContinueWith(_ => { });
            }
        }
    }
}
