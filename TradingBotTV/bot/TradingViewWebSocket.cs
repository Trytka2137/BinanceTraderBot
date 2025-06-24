using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Bot
{
    public static class TradingViewWebSocket
    {
        public static async Task StartAsync()
        {
            if (string.IsNullOrEmpty(ConfigManager.TradingViewWsUrl))
            {
                Console.WriteLine("ℹ️ Nie ustawiono adresu TradingView WebSocket.");
                return;
            }

            while (true)
            {
                using var ws = new ClientWebSocket();
                try
                {
                    await ws.ConnectAsync(new Uri(ConfigManager.TradingViewWsUrl), CancellationToken.None);
                    Console.WriteLine("\uD83D\uDD0C Połączono z TradingView WS");
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
                        Console.WriteLine($"\uD83C\uDF10 TradingView: {msg}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd WebSocket TradingView: {ex.Message}");
                }

                Console.WriteLine("↺ Ponawiam połączenie z TradingView za 30s...");
                await Task.Delay(TimeSpan.FromSeconds(30));
            }
        }
    }
}
