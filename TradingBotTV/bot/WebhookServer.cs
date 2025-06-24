using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using Newtonsoft.Json.Linq;
using System.Threading.Tasks;

using System;
using System.IO;
namespace Bot
{
    public static class WebhookServer
    {
        public static void Start()
        {
            var builder = WebApplication.CreateBuilder();
            var app = builder.Build();

            app.MapPost("/webhook", async (HttpContext context) =>
            {
                try
                {
                    using var reader = new StreamReader(context.Request.Body);
                    var body = await reader.ReadToEndAsync();
                    var json = JObject.Parse(body);
 hm8wp8-codex/sprawdź-poprawność-kodu
                    var signal =
                        (string?)json["strategy"]? ["order_action"] ??
                        (string?)json["action"] ??
                        (string?)json["signal"];
                    var pair = json["ticker"]?.ToString() ?? json["symbol"]?.ToString();

                    Console.WriteLine($"📩 Otrzymano sygnał: {signal} dla {pair}");

                    var signal = json["signal"]?.ToString();

                    Console.WriteLine($"📩 Otrzymano sygnał: {signal}");
 BOT

                    if (signal == "buy" || signal == "sell")
                    {
                        var trader = new BinanceTrader();
 hm8wp8-codex/sprawdź-poprawność-kodu
                        await trader.ExecuteTrade(signal, pair);

                        await trader.ExecuteTrade(signal);
 BOT
                    }

                    await context.Response.WriteAsync("OK");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Błąd obsługi webhooka: {ex.Message}");
                    context.Response.StatusCode = 400;
                    await context.Response.WriteAsync("Error");
                }
            });

            app.Run("http://localhost:5000");
        }
    }
}
