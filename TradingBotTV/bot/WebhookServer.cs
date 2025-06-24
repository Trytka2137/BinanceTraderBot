using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using Newtonsoft.Json.Linq;
using System.Threading.Tasks;

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
                using var reader = new StreamReader(context.Request.Body);
                var body = await reader.ReadToEndAsync();
                var json = JObject.Parse(body);
                var signal = json["signal"]?.ToString();

                Console.WriteLine($"📩 Otrzymano sygnał: {signal}");

                if (signal == "buy" || signal == "sell")
                {
                    var trader = new BinanceTrader();
                    await trader.ExecuteTrade(signal);
                }

                await context.Response.WriteAsync("OK");
            });

            app.Run("http://localhost:5000");
        }
    }
}
