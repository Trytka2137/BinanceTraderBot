using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using Newtonsoft.Json.Linq;
using System.Threading.Tasks;
using System.Threading;

using System;
using System.IO;
namespace Bot
{
    public static class WebhookServer
    {
        public static void Start(CancellationToken token)
        {
            var builder = WebApplication.CreateBuilder();
            var app = builder.Build();

            var tokenValue = Environment.GetEnvironmentVariable("WEBHOOK_TOKEN");

            app.MapPost("/webhook", async (HttpContext context) =>
            {
                try
                {
                    if (!string.IsNullOrEmpty(tokenValue))
                    {
                        if (!context.Request.Headers.TryGetValue("X-BOT-TOKEN", out var hdr) || hdr != tokenValue)
                        {
                            context.Response.StatusCode = 401;
                            await context.Response.WriteAsync("Unauthorized");
                            return;
                        }
                    }
                    using var reader = new StreamReader(context.Request.Body);
                    var body = await reader.ReadToEndAsync();
                    var json = JObject.Parse(body);
                    var signal =
                        (string?)json["strategy"]? ["order_action"] ??
                        (string?)json["action"] ??
                        (string?)json["signal"];
                    var pair = json["ticker"]?.ToString() ?? json["symbol"]?.ToString();

                    Console.WriteLine($"📩 Otrzymano sygnał: {signal} dla {pair}");

                    if (signal == "buy" || signal == "sell")
                    {
                        var trader = new BinanceTrader();
                        await trader.ExecuteTrade(signal, pair, 0m);
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

            app.RunAsync("http://localhost:5000", token).GetAwaiter().GetResult();
        }
    }
}
